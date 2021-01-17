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

import rulebook

class SvParser:

  from sv_file_functions import\
    load_sv_file,\
    find_rtl_folders,\
    find_sv_files

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
    get_module_instances,\
    get_module_instances_without_parameters,\
    get_module_instances_with_parameters

  from sv_rtl_tree import\
    list_all_modules,\
    print_all_modules,\
    find_top_modules,\
    print_top_modules,\
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

  def __init__(self, yml_rules):
    self.rules = rulebook.RuleBook()
    self.rules.load_rules(yml_rules)
    #self.rules.print_rules()

  def pretty(self, sv_file):

    self.load_sv_file(sv_file)
    self.format_file()
