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

import os, sys, subprocess, time
import argparse
import sv_parser

# Pretty System Verilog
def psv():

  _start_time = time.time()


  format_file(svparser)
  # Create the RTL tree
  #rtl_tree(svparser, os.getcwd())
  #svparser.print_all_modules()

  print("INFO [rtl_tree] Completed in (%s) seconds" % "{:.3f}".format((time.time() - _start_time)))


  #pretty(svparser)
  #detect_submodule(svparser)

def format_file(svparser):
  git_root = svparser.get_git_root()
  svparser.load_sv_file(git_root + "/psv/rtl/top.sv")
  svparser.format_file()

def pretty(svparser):
  svparser.pretty("/home/erland/Documents/pretty_system_verilog/psv/rtl/top.sv")

def rtl_tree(svparser, pwd):
  svparser.rtl_tree(pwd)

def list_all_modules(svparser):
  svparser.list_all_modules("/home/erland/Documents/pretty_system_verilog/psv")

def find_rtl_folders(svparser):
  found = svparser.find_rtl_folders("/home/erland/Documents/pretty_system_verilog/psv")
  for f in found:
    print(f)

def detect_submodule(svparser):

  svparser.load_sv_file("/mnt/work/freake/zip_dev/modules/ziptilion/rtl/ziptilion_core.sv")
  found = svparser.detect_submodule()
  for f in found:

    _instantiation = f[0]
    module_type    = f[1]
    instance_name  = f[2]

    print("%s %s" % (module_type, instance_name))

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

def get_git_root():
  _is_git = subprocess.Popen(['git', 'rev-parse', '--is-inside-work-tree'],
                           stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
  if _is_git:
    return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                             stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
  else:
    return ""


if __name__ == '__main__':

  _git = get_git_root()

  parser = argparse.ArgumentParser()
  parser.add_argument("-e", "--example",   action="store_true",        help = "Print example command")
  parser.add_argument("-r", "--rtl_tree",  type = int, default = 0,    help = "Print an RTL-Tree",                               metavar=' ')
  parser.add_argument("-d", "--dir",       type = str, default = _git, help = "Root directory of modules, default git toplevel", metavar=' ')
  parser.add_argument("-f", "--file",      type = str, default = "",   help = "The file to format pretty",                       metavar=' ')
  parser.add_argument("-y", "--yml",       type = str, default = "",   help = "The YML file containing custom format rules",     metavar=' ')
  parser.add_argument("-v", "--verbosity", type = int, default = 0,    help = "Increase output verbosity",                       metavar=' ')

  args = parser.parse_args()

  # RTL Tree
  if args.rtl_tree:
    svparser = sv_parser.SvParser(verbosity=args.verbosity)

  # Format a file
  elif args.file:
    rules_file = args.yml

    if not os.path.isfile(args.file):
      print("ERROR [psv] File (%s) does not exist" % args.file)
      sys.exit(-1)

    if not args.file.endswith("_pkg.sv"):
      print("ERROR [psv] File [-f] must end with (.sv)" % args.file)
      sys.exit(-1)

    if not os.path.isfile(rules_file):
      rules_file = os.path.join(sys.path[0], "rules.yml")
      if not os.path.isfile(rules_file):
        print("ERROR [psv] File (%s) does not exist" % args.yml)
        sys.exit(-1)

    svparser = sv_parser.SvParser(yml_rules=args.yml, verbosity=args.verbosity)
    svparser.load_sv_file(args.file)

  else:
    print("INFO [psv] Arguments must be provided")
