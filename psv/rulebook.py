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
import sv_keywords

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
class RuleBook:

  def load_rules(self, yml_file):

    # Open the file
    with open(yml_file, 'r') as file:
      _fh = yaml.load(file, Loader = yaml.FullLoader)
      _, self.rules = list(_fh.items())[0]

    # Load the rules into the rule book
    self.r_module_indentation  = self.rules["module_indentation"]["value"]
    self.r_global_indentation  = self.rules["global_indentation"]["value"]
    self.r_collect_logics      = self.rules["collect_logics"]["value"]
    self.r_collect_assignments = self.rules["collect_assignments"]["value"]
    self.r_allow_key_reg       = self.rules["allow_key_reg"]["value"]
    self.r_allow_key_wire      = self.rules["allow_key_wire"]["value"]
    self.r_localparam_types    = self.rules["localparam_types"]["value"]
    self.r_parameter_types     = self.rules["parameter_types"]["value"]
    self.r_comment_head        = self.rules["comment_head"]["value"]
    self.r_bracket_spaces_in   = self.rules["bracket_spaces_in"]["value"]
    self.r_bracket_spaces_out  = self.rules["bracket_spaces_out"]["value"]
    self.r_bracket_adjust      = self.rules["bracket_adjust"]["value"]

  def print_rules(self):

    print("module_indentation  = %d" % self.r_module_indentation)
    print("global_indentation  = %d" % self.r_global_indentation)
    print("collect_logics      = %s" % self.r_collect_logics)
    print("collect_assignments = %s" % self.r_collect_assignments)
    print("allow_key_reg       = %s" % self.r_allow_key_reg)
    print("allow_key_wire      = %s" % self.r_allow_key_wire)
    print("localparam_types    = %s" % self.r_localparam_types)
    print("parameter_types     = %s" % self.r_parameter_types)
    print("comment_head        = %d" % self.r_comment_head)
    print("bracket_spaces_in   = %d" % self.r_bracket_spaces_in)
    print("bracket_spaces_out  = %d" % self.r_bracket_spaces_out)
    print("bracket_adjust      = %s" % self.r_bracket_adjust)

  def is_keyword(self, word):
    return word in sv_keywords.sv_keywords

  def get(self, rule):
    return self.rules[rule]["value"]
