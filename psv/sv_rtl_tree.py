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

import time
from treelib import Node, Tree

# ------------------------------------------------------------------------------
# A recursive function which generates branches of a module's all submodules
# ------------------------------------------------------------------------------
def rtl_branch(self, name, parent_id, instance_name, hier_nr, print_instance=False):

  _node_id = self.tree_counter
  self.tree_counter += 1

  _tag = name
  if print_instance:
    _tag = _tag.ljust(60-hier_nr*4) + " (%s)" % instance_name

  #create_node(tag=None, identifier=None, parent=None, data=None)
  self.tree.create_node(_tag, str(_node_id), parent=str(parent_id), data=instance_name)

  for i in range(len(self.all_modules[name])):
    _mod, _ins = self.all_modules[name][i]
    if _mod in self.all_modules: # TODO: Still needed?
      self.rtl_branch(_mod, _node_id, _ins.strip(), hier_nr+1, print_instance)


# ------------------------------------------------------------------------------
# Generates the parent in the tree by finding the top module in the current
# working directory, i.e., the path provided as the argument "pwd"
# ------------------------------------------------------------------------------
def rtl_tree(self, pwd):

  # Find all the top module and print them if verbosity is high
  _pwd_tops = self.find_top_modules(pwd)
  if self.verbosity >= 1000:
    print("DEBUG [rtl_tree] Top modules in the selected directory:")
    for _t in _pwd_tops:
      print(_t)

  # How many tops that will be rendered is configurable
  if len(self.tops) > self.cfg_tree_max_tops:
    print("ERROR [rtl_tree] More than (%d) top module found!" % self.cfg_tree_max_tops)
    return -1

  # Generate and print out the RTL Tree of all the tops
  for t in range(len(self.tops)):

    _rtl_top = _pwd_tops[t]

    print(80*'-')
    print("- RTL Tree of \"%s\"" % _rtl_top)
    print(80*'-')

    self.tree = Tree()
    self.tree.create_node(_rtl_top, str(0))
    self.tree_counter = 1

    for i in range(len(self.all_modules[_rtl_top])):
      _m, _i = self.all_modules[_rtl_top][i]
      if _m in self.all_modules:
        self.rtl_branch(_m, 0, _i.strip(), 1, True)

    self.tree.show()
    print('\n')
