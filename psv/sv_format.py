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

def format_file(self):

  name, m              = self.format_module(self.get_module())
  always_ff            = self.format_always_ff(self.get_always_ff())
  always_comb          = self.format_always_comb(self.get_always_comb())
  logic_declarations   = self.format_logic_declarations(self.get_logic_declarations())
  assign_declarations  = self.format_assign_declarations(self.get_assign_declarations())
  module_instances     = self.format_module_instances(self.get_module_instances())
  typedef_declarations = self.format_typedef_declarations(self.get_typedef_declarations())
  custom_declarations  = self.format_custom_declarations(self.get_custom_declarations())

  print("INFO [pretty] Formatting \"%s\"" % name)
  print(m)
  print(always_ff)
  print(always_comb)
  print(logic_declarations)
  print(assign_declarations)
  print(module_instances)
  print(typedef_declarations)
  print(custom_declarations)


def format_module(self, module):
  return module


def format_always_ff(self, always_ff):
  return always_ff


def format_always_comb(self, always_comb):
  return always_comb


def format_logic_declarations(self, logic_declarations):
  return logic_declarations


def format_assign_declarations(self, assign_declarations):
  return assign_declarations


def format_module_instances(self, module_instances):
  return module_instances


def format_typedef_declarations(self, typedef_declarations):
  return typedef_declarations


def format_custom_declarations(self, custom_declarations):
  return custom_declarations

