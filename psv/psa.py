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
  _pwd = os.getcwd()

  parser = argparse.ArgumentParser()
  parser.add_argument("-e", "--example",   action="store_true",        help = "Print example command")
  parser.add_argument("-r", "--rtl_tree",  type = int, default = 0,    help = "Print an RTL-Tree",                               metavar=' ')
  parser.add_argument("-p", "--dir",       type = str, default = _git, help = "Root directory of modules, default git toplevel", metavar=' ')
  parser.add_argument("-f", "--file",      type = str, default = "",   help = "The file to format pretty",                       metavar=' ')
  parser.add_argument("-y", "--yml",       type = str, default = "",   help = "The YML file containing custom format rules",     metavar=' ')
  parser.add_argument("-v", "--verbosity", type = int, default = 0,    help = "Increase output verbosity",                       metavar=' ')
  parser.add_argument("-d", "--develop",   action="store_true",        help = "Do some development function")

  args = parser.parse_args()

  # Develop
  if args.develop:
    _yml      = os.path.join(sys.path[0], "rules.yml")
    _svparser = sv_parser.SvParser(_yml, verbosity=2)
    _svparser.load_sv_file(_git + "/psv/rtl/top.sv", rm_comments=False)
    _svparser.format_file()

  # RTL Tree
  elif args.rtl_tree:
    svparser = sv_parser.SvParser(verbosity=args.verbosity)
    svparser.rtl_tree(_pwd)

  # Format a file
  elif args.file:
    rules_file = args.yml

    # The file to format must exist
    if not os.path.isfile(args.file):
      print("ERROR [psv] File (%s) does not exist" % args.file)
      sys.exit(-1)

    # The file must be System Verilog
    if not args.file.endswith(".sv"):
      print("ERROR [psv] File [-f] must end with (.sv)" % args.file)
      sys.exit(-1)

    # The rules file must exist TODO: Default?
    if not os.path.isfile(rules_file):
      rules_file = os.path.join(sys.path[0], "rules.yml")
      if not os.path.isfile(rules_file):
        print("ERROR [psv] File (%s) does not exist" % args.yml)
        sys.exit(-1)

    svparser = sv_parser.SvParser(yml_rules=args.yml, verbosity=args.verbosity)
    svparser.load_sv_file(args.file)

  else:
    print("INFO [psv] Arguments must be provided")
