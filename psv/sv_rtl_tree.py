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

from treelib import Node, Tree

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def rtl_branch(self, name, parent_id, instance_name, hier_nr, print_instance=0):

  _node_id = self.tree_counter
  self.tree_counter += 1

  _tag = name
  if print_instance:
    _tag = _tag.ljust(60-hier_nr*4) + " (%s)" % instance_name

  #create_node(tag=None, identifier=None, parent=None, data=None)
  self.tree.create_node(_tag, str(_node_id), parent=str(parent_id), data=instance_name)

  for i in range(len(self.all_modules[name])):
    _m, _i = self.all_modules[name][i]
    if _m not in self.all_interfaces and _m != "riq_entry_t":
      self.rtl_branch(_m, _node_id, _i.strip(), hier_nr+1, print_instance)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def rtl_tree(self, pwd, instance_name=0):

  _pwd_tops = self.find_top_modules(pwd)
  print("_pwd_tops: ")
  print(_pwd_tops)

  _max_tops = 1
  if len(self.tops) > _max_tops:
    print("ERROR [rtl_tree] More than (%d) top module found!" % _max_tops)
    return -1

  _rtl_top = _pwd_tops[0]

  print(80*'-')
  print("RTL Tree of \"%s\"" % _rtl_top)
  print(80*'-')

  self.tree = Tree()
  self.tree.create_node(_rtl_top, str(0))
  self.tree_counter = 1

  for i in range(len(self.all_modules[_rtl_top])):
    _m, _i = self.all_modules[_rtl_top][i]
    if _m not in self.all_interfaces:
      self.rtl_branch(_m, 0, _i.strip(), 1, True)

  self.tree.show()
