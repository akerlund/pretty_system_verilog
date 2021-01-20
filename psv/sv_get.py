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
def detect_submodule(self, top_type):

  mod = []
  def detect(regex):
    for m in re.findall(regex, self.flat):
      sub_type = m[0]
      if sub_type != top_type:
        mod.append(m)

  # These expressions stops after a found instance name
  # First (e0) is for without parameters and the second (e1) with parameters
  e0 = r'\n+\s*(\w+)\s+(\w+)\s*\([\s.\w_(),/[\]]*\)\s*;'
  e1 = r"\n+\s*(\w+)\s*#\s*\([\s.\w_(),/[\]]*\)\s*\)\s*(\w+)\s*\("

  # Everything
  #e2 = r'\n+\s*(\w+)\s*#\s*\([\s.\w_(),/]*\)\s*\)\s*(\w+)\s*\([\s.\w_(),/]*\)\s*;'
  detect(e0)
  detect(e1)


  return mod