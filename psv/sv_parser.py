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

import os, sys
import rulebook
import yaml

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
class SvParser:

  from sv_file_functions import\
    load_sv_file,\
    find_rtl_folders,\
    find_sv_files,\
    is_directory,\
    make_directory,\
    file_exists,\
    get_git_root,\
    remove_comments

  from sv_get import\
    get_always_ff,\
    get_always_comb,\
    get_always_x,\
    get_comment_pre_offset,\
    get_module,\
    get_from_begin_to_end,\
    get_to_semicolon,\
    get_logic_declarations,\
    words_exist_in_string,\
    get_assign_declarations,\
    get_typedef_declarations,\
    get_custom_declarations,\
    get_all_brackets,\
    detect_submodule

  from sv_rtl_tree import\
    rtl_tree,\
    rtl_branch

  from sv_format import\
    format_file,\
    format_module,\
    format_always_ff,\
    format_always_comb,\
    format_logic_declarations,\
    format_assign_declarations,\
    format_module_instances,\
    format_typedef_declarations,\
    format_custom_declarations

  from sv_print import\
    print_all_modules,\
    print_top_modules

  from sv_module_list import\
    list_all_modules,\
    get_modules_in_folder,\
    find_top_modules

  # ----------------------------------------------------------------------------
  #
  # ----------------------------------------------------------------------------
  def __init__(self, yml_rules = "", verbosity = 0):

    self.verbosity = verbosity
    self.load_cfg()

    if yml_rules:
      self.rules = rulebook.RuleBook()
      self.rules.load_rules(yml_rules)
      #self.rules.print_rules()

    # TODO: If no module path, set it to git repository
    self.list_all_modules(self.cfg_module_root)

    #self.print_all_modules(table=True)
    #self.print_all_modules(print_sub=True)


  def pretty(self, sv_file):

    self.load_sv_file(sv_file)
    self.format_file()


  def load_cfg(self):

    # Default configuration values
    self.module_paths = []
    self.cfg_search_paths = False

    # The config file should be local to this script
    cfg_file = os.path.join(sys.path[0], "config.yml")

    # Default if the file does not exist
    if not self.file_exists(cfg_file):
      print("ERROR [load_cfg] Config file not found")
      return -1

    # Open the file
    with open(cfg_file, 'r') as _file:
      _fh = yaml.load(_file, Loader = yaml.FullLoader)
      _, self.rules = list(_fh.items())[0]

    # Append the seach paths and replace any git root string
    _module_path = self.rules["module_paths"]["value"]
    _git_root    = self.get_git_root()

    self.cfg_module_root   = _module_path.replace("${git_root}", _git_root)
    self.cfg_search_paths  = self.rules["search_paths"]["value"]
    self.cfg_tree_max_tops = 1

