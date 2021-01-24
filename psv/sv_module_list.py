################################################################################
##
## Copyright (C) 2021 Fredrik Åkerlund
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <https:##www.gnu.org/licenses/>.
##
## Description:
##
################################################################################

import time, sys
import sv_keywords

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def list_all_modules(self, root_folder):

  if self.verbosity >= 1000:
    print("DEBUG [list_all_modules] Root folder: (%s)" % root_folder)
    print("DEBUG [list_all_modules] RTL folders:")

  # Find all System Verilog files
  _all_sv_files = []
  for _f in self.find_rtl_folders(root_folder):
    if self.verbosity >= 1000:
      print("DEBUG [list_all_modules] RTL folder: (%s)" % _f)
    _all_sv_files += self.find_sv_files(_f, exclude_pkg=1)
  _nr_of_files = len(_all_sv_files)

  # Variables for modules and interfaces
  self.all_modules    = {}
  self.all_interfaces = []

  _start_time = time.time()

  # Iterate all the found System Verilog files
  _i = 1
  for sv in _all_sv_files:

    if self.verbosity >= 2:
      sys.stdout.write("\rProcessing file (%d/%d): %s\x1b[K" % (_i, _nr_of_files, sv))
      sys.stdout.flush()
      _i += 1

    # Load the file
    self.load_sv_file(sv)

    # Get the module's name
    _module_name = self.get_module(only_name=1)

    # Check the length because a file does not need to have a module
    if len(_module_name):

      if _module_name in self.all_modules.keys():
        print("WARNING [list_all_modules] Module (%s) already found, skipping" % _module_name)
      else:

        # Initialize dictionary
        self.all_modules[_module_name] = []

        # Get the submodules' in this module
        for _sub in self.detect_submodule(_module_name):

          _module_type   = _sub[0]
          _instance_name = _sub[1]

          # Catches, e.g., "else", "task" and "module"
          _m_ok = (not _module_type in sv_keywords.sv_keywords)

          if _m_ok:
            if _instance_name == "":
              print("WARNING [list_all_modules] Found no instance name for (" + _module_name + "." + _module_type)
            self.all_modules[_module_name].append((_module_type, _instance_name))
          else:
            if _module_type == "interface":
              print("interface: %s" % _instance_name)
              self.all_interfaces.append(_instance_name)
            # TODO: Perhaps improve so this does not occur
            #else:
            #  print("WARNING [detect_submodule] Incorrect type, a SV key: (%s)" % _module_type)

  if self.verbosity >= 2:
    print('\n')
    print("INFO [list_all_modules] Completed in (%s) seconds" % "{:.3f}".format((time.time() - _start_time)))
    print("INFO [list_all_modules] Nr of modules:    (%s)" % len(self.all_modules))
    print("INFO [list_all_modules] Nr of interfaces: (%s)" % len(self.all_interfaces))

  if self.verbosity >= 1000:
    self.print_all_modules(print_sub=True, table=False)
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_modules_in_folder(self, root_folder):

  _modules = {}

  # Find all System Verilog files
  for _rtl_folder in self.find_rtl_folders(root_folder):

    sv_files = self.find_sv_files(_rtl_folder, exclude_pkg=1)

    # Iterate all the found System Verilog files
    for sv in sv_files:

      # Load the file
      self.load_sv_file(sv, rm_comments=False)

      # Get the module's name
      _m_name           = self.get_module(only_name=1)
      if not _m_name:
        print("ERROR [get_modules_in_folder] Module with zero length name found in:\n%s%s" % (30*' ', sv))
      else:
        _modules[_m_name] = self.all_modules[_m_name]

  return _modules


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def find_top_modules(self, pwd = ""):

  self.tops   = []
  self.tops_n = []

  _tops   = []
  _tops_n = []

  # If we only want to find top modules inside the local directory (pwd),
  # we must first list all modules
  _pwd   = not(pwd == "")
  _pwd_m = None

  if _pwd:
    _pwd_m = self.get_modules_in_folder(pwd)


  if self.verbosity >= 1000:
    self.print_all_modules()
    print("DEBUG [find_top_modules] Local modules in (%s):" % pwd)
    for _key in _pwd_m:
      print(_key)

  # Decide which module list to use and find top modules in
  if _pwd:
    _modules = _pwd_m
  else:
    _modules = self.all_modules

  # We do a search through the list to see if a module (_k0) exists
  # in another module's (_k1) submodule list
  for _k0 in _modules:
    if _pwd:
      if _k0 in _pwd_m:
        _is_top = True
      for _k1 in _modules:
        for _m, _i in _modules[_k1]:
          if _k0 == _m:
            _is_top = False
            # Only append to the non-top list when we are not running local
            if not _pwd:
              self.tops_n.append(_k0)
            break
      if _is_top:
        # Decide which list to append to
        if not _pwd:
          self.tops_n.append(_k0)
        else:
          _tops.append(_k0)

  if self.verbosity >= 1000:
    print("DEBUG [find_top_modules] Top modules in the selected directory:")
    for _t in _tops:
      print(_t)

  # Local gives a return
  if _pwd:
    return _tops
