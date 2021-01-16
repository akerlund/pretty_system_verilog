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

def list_all_modules(self, root_folder):

  _rtl_folders     = self.find_rtl_folders(root_folder)
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
      self.all_modules[module_name] = []

      #print("\n\nModule: " + module_name)
      for f in module_instances:
        module_type   = f[1]
        #instance_name = f[2]
        self.all_modules[module_name].append(module_type)


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
      for s in sub:
        print("  " + s)


def find_top_modules(self):

  self.tops   = []
  self.tops_n = []

  for _k0 in self.all_modules:
    _is_top = True
    for _k1 in self.all_modules:
      if _k0 in self.all_modules[_k1]:
        _is_top = False
        self.tops_n.append(_k0)
        break
    if _is_top:
      self.tops.append(_k0)


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


def rtl_branch(self, name, n, last, left):

  if left:
    branch = n*"| " + name + "\n"
  else:
    branch = ""

  _len  = len(self.all_modules[name])
  _last = False
  _left = _len-1

  if _len != 0:
    branch += (n)*' ' + "|" + "\n"
    if not last:
      branch += (n*3-1)*' ' + " +-"
    else:
      branch += (n*3-1)*' ' + " `-"




  for i in range(len(self.all_modules[name])):
    if i == _len-1:
      _last = True
    branch += self.rtl_branch(self.all_modules[name][i], n+1, _last, _left) + "\n"

  return branch


def rtl_tree(self, folder):


  self.list_all_modules(folder)
  self.find_top_modules()
  self.print_all_modules()
  self.print_top_modules()

  if len(self.tops) != 1:
    print("ERROR [rtl_tree] More than one top module found!")
    return -1

  rtl_tree  = self.tops[0] + "\n"

  print(80*'-')
  print("RTL Tree of \"%s\"" % self.tops[0])
  print(80*'-')
  _len  = len(self.all_modules[self.tops[0]])
  _last = False
  _left = _len -1
  for i in range(len(self.all_modules[self.tops[0]])):
    rtl_tree += "|" + "\n"
    if i == _len-1:
      rtl_tree += "`-"
      _last = True
    else:
      rtl_tree += "+-"
    rtl_tree += self.rtl_branch(self.all_modules[self.tops[0]][i], 1, _last, _left)
    rtl_tree += "D\n"

  print(rtl_tree)



