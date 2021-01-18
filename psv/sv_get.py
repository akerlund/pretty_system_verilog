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

import re
import sv_keywords

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_always_ff(self):
  return self.get_always_x(r'always_ff')


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_always_comb(self):
  return self.get_always_x(r'always_comb')


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_always_x(self, exp):
  found = []
  for i in range(len(self.svf)):
    match = re.search(exp, self.svf[i])
    if match:
      b_to_e, _ = self.get_from_begin_to_end(i)
      # get_comment_pre_offset
      found.append(b_to_e)
  return found


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_comment_pre_offset(self, offset):
  return ""


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_module(self, only_name = 0):

  _i = -1
  mod = ""

  for i in range(len(self.svf)):
    match = re.search(r'^\s*module (\w+)(\s*#?|\s*\(?)', self.svf[i])
    if match:
      _i = i
      name = match.group(1)
      if only_name:
        return name

  if _i == -1:
    print("ERROR [module] No module found in file (%s)", self.current_file)
    return ""

  for i in range(len(self.svf)):
    _row = self.svf[i].split("//")[0]
    _f   = _row.find(");")
    if _f >= 0:
      mod += _row[:_f+2] + '\n' # All characters including ");"
      break
    mod += self.svf[i] + '\n'

  return name, mod


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_from_begin_to_end(self, offset):

  r = "" # Return
  b = 0  # Number of found 'begin'
  e = 0  # Number of found 'end'
  c = 0  # Number of iterated rows, a counter

  for row in self.svf[offset:]:
    _row = row.split("//")[0]
    b += _row.count("begin")
    e += _row.count("end")
    r += _row + '\n'
    if b != 0 and b == e:
      break
    c += 1

  return r, c


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_to_semicolon(self, offset):

  r = "" # Return
  c = "" # Tailing comment
  for row in self.svf[offset:]:
    _row = row.split("//")[0]
    _f   = _row.find(";")
    if _f >= 0:
      r += _row[:_f+1]
      c  = _row[_f+1:]
      break
  return r, c


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_logic_declarations(self):

  illegal_words = ["parameter", "input", "output", "localparam"]
  logics = []

  for i in range(len(self.svf)):
    _row = self.svf[i].split("//")[0]
    _f   = _row.find("logic")
    if _f >= 0:
      if not self.words_exist_in_string(_row, illegal_words):
        logics.append(self.get_to_semicolon(i))
  return logics


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def words_exist_in_string(self, string, words):

  for word in words:
    if string.count(word) != 0:
      return True
  return False


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_assign_declarations(self):

  assigns = []

  for i in range(len(self.svf)):
    _row = self.svf[i].split("//")[0]
    match = re.search(r'^\s*assign\s+', self.svf[i])
    if match:
      assigns.append(self.get_to_semicolon(i))
  return assigns


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_typedef_declarations(self):
  return []


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_custom_declarations(self):
  return []


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_all_brackets(self, row):

  brackets = []
  match = re.findall(r'(\[.*?\])', row)
  if match:
    for m in match:
      brackets.append(m)
  return brackets


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_submodule_instances(self):
  # TODO: Add support for ';' in comments
  return self.get_submodule_instances_without_parameters() +\
         self.get_submodule_instances_with_parameters()


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_submodule_instances_without_parameters(self):
  e = r'((\w+)\s+(\w+)\s*\(([.|\w|\s|,|\/|\)|\(]*)\);)'
  mod = []
  for m in re.findall(e, self.flat):
    module_type = m[1]
    if module_type != "module":
      mod.append(m)
  return mod


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_submodule_instances_with_parameters(self):
  # ((\w+)\s*#\s*\([\w\W]+?(?=\)\s*\;))
  e = r'((\w+)\s*#\s*\(\s*.+[\w\W]*\)(\s*\w+\s*)\(\s*.+[\w\W]*\);)'
  mod = []
  for m in re.findall(e, self.flat):
    module_type = m[1]
    if module_type != "module":
      mod.append(m)
  return mod


# ------------------------------------------------------------------------------
# Detects submodule syntaxes and compares the type with the list of types, i.e.,
# self.all_modules.keys() and return all valid in a list.
# ------------------------------------------------------------------------------
def detect_submodule(self, top_type):

  e0 = r'\s*(\w+)\s+(\w+)\s*\('                   # Without parameter
  e1 = r'\s*(\w+)\s*#\(.*|\s\)\s*\)\s*(\w+)\s*\(' # With parameter
  mod = []

  for m in re.findall(e0, self.flat):

    module_type = m[0]

    if module_type in self.all_modules.keys():
      if module_type == top_type:
        print("WARNING [detect_submodule] Recursive add: (%s)" % module_type)
      else:
        mod.append(m)

  for m in re.findall(e1, self.flat):

    module_type = m[0]

    if module_type in self.all_modules.keys():
      if module_type == top_type:
        print("WARNING [detect_submodule] Recursive add: (%s)" % module_type)
      else:
        mod.append(m)


  return mod
