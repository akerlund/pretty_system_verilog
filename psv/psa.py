#!/usr/bin/env python3

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

import yaml
import sys, os

import rulebook

import sv_parser

# Pretty System Verilog
def psv():

  rules = rulebook.RuleBook()
  rules.load_rules("/home/erland/Documents/pretty_system_verilog/psv/rules.yml")
  rules.print_rules()

  if rules.is_keyword("module"):
    print("module is a keyword")
  else:
    print("module is not a keyword")

  svparser = sv_parser.SvParser()
  svparser.load_sv_file("/home/erland/Documents/pretty_system_verilog/psv/rtl/top.sv")

  rtl_tree(svparser)
  #get_module(svparser)

def rtl_tree(svparser):
  svparser.rtl_tree("/home/erland/Documents/pretty_system_verilog/psv")

def list_all_modules(svparser):
  svparser.list_all_modules("/home/erland/Documents/pretty_system_verilog/psv")

def find_rtl_folders(svparser):
  found = svparser.find_rtl_folders("/home/erland/Documents/pretty_system_verilog/psv")
  for f in found:
    print(f)

def get_module_instances(svparser):
  found = svparser.get_module_instances()
  for f in found:

    instantiation = f[0]
    module_type   = f[1]
    instance_name = f[2]

    print("\n\nThis is %s of type %s:" % (instance_name, module_type))
    print(instantiation)

def get_assign_declarations(svparser):
  found = svparser.get_assign_declarations()
  for f in found:
    print(' '.join(f))

def get_logic_declarations(svparser):
  found = svparser.get_logic_declarations()
  for r, _ in found:
    print(r)

def get_module(svparser):
  name, body = svparser.get_module()
  print("name = \"" + name + "\"")
  print(body)

def get_always_comb(svparser):
  found = svparser.get_always_comb()
  for f in found:
    print(f)

def get_always_ff(svparser):
  found = svparser.get_always_ff()
  for f in found:
    print(f)

if __name__ == '__main__':
  psv()