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

import os
from treelib import Node, Tree
import sv_keywords

def list_all_modules(self, root_folder, is_pwd=False):

  _rtl_folders = self.find_rtl_folders(root_folder)

  print("RTL folders:")
  print(_rtl_folders)

  if is_pwd:
    _all_modules = {}
  else:
    self.all_modules = {}

  # Find all System Verilog files
  for _f in _rtl_folders:
    sv_files = self.find_sv_files(_f, exclude_pkg=1)

    # Load one System Verilog file at the time
    for sv in sv_files:
      self.load_sv_file(sv)

      # Get the module's name
      module_name = self.get_module(only_name=1)

      # Get the submodules in the module
      module_instances = self.get_module_instances()

      # Instantiate a dictionary for this module
      if is_pwd:
        _all_modules[module_name] = []
      else:
        self.all_modules[module_name] = []

      #print("\n\nModule: " + module_name)
      for f in module_instances:

        module_type   = f[1]
        instance_name = f[2]

        if not module_type in sv_keywords.sv_keywords:
          if is_pwd:
            _all_modules[module_name].append((module_type, instance_name))
          else:
            self.all_modules[module_name].append((module_type, instance_name))

  if is_pwd:
    return _all_modules


def print_all_modules(self):

  print(80*'-')
  print("- All (%d) modules" % len(self.all_modules))
  print(80*'-')

  for key in self.all_modules:
    sub = self.all_modules[key]
    print("\n\nModule: " + key)
    if not len(sub):
      print("  - No submodules")
    else:
      for module_type, _ in sub:
        print("  " + module_type)


def find_top_modules(self, pwd = ""):

  self.tops   = []
  self.tops_n = []

  _tops   = []
  _tops_n = []

  # If we only want to find top modules inside the local directory (pwd),
  # we must first list all modules
  _pwd = not(pwd == "")
  _pwd_m = []
  if _pwd:
    _pwd_m = self.list_all_modules(pwd, is_pwd=True)

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


def print_top_modules(self):

  print(80*'-')
  print("- All (%d) tops" % len(self.tops))
  print(80*'-')
  for t in self.tops:
    print(t)

  print("\n\n")
  print(80*'-')
  print("- All (%d) non-tops" % len(self.tops_n))
  print(80*'-')
  for t in self.tops_n:
    print(t)


def rtl_branch(self, name, parent_id, instance_name, hier_nr, print_instance=0):

  _node_id = self.tree_counter
  self.tree_counter += 1

  _tag = name
  if print_instance:
    _tag = _tag.ljust(60-hier_nr*4) + " (%s)" % instance_name

  #create_node(tag=None, identifier=None, parent=None, data=None)
  self.tree.create_node(_tag, str(_node_id), parent=str(parent_id), data=instance_name)

  for i in range(len(self.all_modules[name])):
    _m, _i = self.all_modules[name][i]
    self.rtl_branch(_m, _node_id, _i, hier_nr+1, print_instance)


def rtl_tree(self, pwd, instance_name=0):

  _pwd_tops = self.find_top_modules(pwd)
  print("_pwd_tops: ")
  print(_pwd_tops)

  _max_tops = 1
  if len(self.tops) > _max_tops:
    print("ERROR [rtl_tree] More than (%d) top module found!" % _max_tops)
    return -1

  _rtl_top = _pwd_tops[0]

  print(80*'-')
  print("RTL Tree of \"%s\"" % _rtl_top)
  print(80*'-')

  self.tree = Tree()
  self.tree.create_node(_rtl_top, str(0))
  self.tree_counter = 1

  for i in range(len(self.all_modules[_rtl_top])):
    _m, _i = self.all_modules[_rtl_top][i]
    self.rtl_branch(_m, 0, _i, 1, True)

  self.tree.show()
