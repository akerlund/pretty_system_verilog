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

class RuleBook:

  def load_rules(self, yml_file):

    # Open the file
    with open(yml_file, 'r') as file:
      _fh = yaml.load(file, Loader = yaml.FullLoader)
      _, self.rules = list(_fh.items())[0]

    # Load the rules into the rule book
    self.module_indentation  = self.rules["module_indentation"]["value"]
    self.global_indentation  = self.rules["global_indentation"]["value"]
    self.collect_logics      = self.rules["collect_logics"]["value"]
    self.collect_assignments = self.rules["collect_assignments"]["value"]
    self.allow_key_reg       = self.rules["allow_key_reg"]["value"]
    self.allow_key_wire      = self.rules["allow_key_wire"]["value"]

  def print_rules(self):

    print("module_indentation  = %d" % self.module_indentation)
    print("global_indentation  = %d" % self.global_indentation)
    print("collect_logics      = %d" % self.collect_logics)
    print("collect_assignments = %d" % self.collect_assignments)
    print("allow_key_reg       = %d" % self.allow_key_reg)
    print("allow_key_wire      = %d" % self.allow_key_wire)

  def is_keyword(self, word):
    return word in sv_keywords.sv_keywords

  def get(self, rule):
    return self.rules[rule]["value"]
