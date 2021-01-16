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

  self.print_all_modules()


def print_all_modules(self):

  for key in self.all_modules:
    sub = self.all_modules[key]
    print("\n\nModule: " + key)
    if not len(sub):
      print("  - No submodules")
    else:
      for s in sub:
        print("  " + s)


def find_top(self):

  tops = []

  for key in self.all_modules:
    sub = self.all_modules[key]

