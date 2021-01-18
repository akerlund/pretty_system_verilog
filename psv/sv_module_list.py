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

import sv_keywords

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def list_all_modules(self, root_folder):

  # This function will instantiate the dictionary "self.all_modules"
  self.get_all_module_names(root_folder)

  # Also list interfaces and modports
  self.all_interfaces = []
  self.all_modports   = []

  # Find all System Verilog files
  for _rtl_folder in self.find_rtl_folders(root_folder):

    if self.debug >= 2:
      print("DEBUG [list_all_modules] Scanning for files in %s" % _rtl_folder)

    sv_files = self.find_sv_files(_rtl_folder, exclude_pkg=1)

    # Iterate all the found System Verilog files
    for sv in sv_files:

      # Load the file
      self.load_sv_file(sv)

      # Get the module's name
      module_name = self.get_module(only_name=1)

      print("Submodules of %s" % module_name)

      # Get the submodules in the module and iterate them
      for _sub in self.detect_submodule(module_name):

        _module_type   = _sub[0]
        _instance_name = _sub[1]

        print(_module_type)

        _m_ok = (not _module_type in sv_keywords.sv_keywords)

        if _m_ok:
          self.all_modules[module_name].append((_module_type, _instance_name))
        else:
          if _module_type == "interface":
            print("interface: %s" % _instance_name)
            self.all_interfaces.append(_instance_name)
          elif _module_type == "modport":
            self.all_interfaces.append(_instance_name)
            print("modport: %s" % _instance_name)
          else:
            print("WARNING [detect_submodule] Incorrect type, a SV key: (%s)" % _module_type)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_all_module_names(self, root_folder):

  self.all_modules = {}

  # Find all System Verilog files
  for _f in self.find_rtl_folders(root_folder):

    # Load one System Verilog file at the time
    for _sv_file in self.find_sv_files(_f, exclude_pkg=1):

      self.load_sv_file(_sv_file)

      # Get the module's name
      _m_name = self.get_module(only_name=1)

      if len(_m_name):
        # Instance the dictionary with an empty list which is to be filled
        # with the submodules types and instance names
        self.all_modules[_m_name] = []
      else:
        print("WARNING [get_all_module_names] Detected a zero long module name in file:\n  %s" % _sv_file)


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
      self.load_sv_file(sv)

      # Get the module's name
      _m_name           = self.get_module(only_name=1)
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

    # Debug print
    if False:
      self.print_all_modules()
      print("Local modules in (%s):" % pwd)
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

  # Local gives a return
  if _pwd:
    return _tops
