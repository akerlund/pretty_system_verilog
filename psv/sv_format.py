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
def format_file(self):

  _module = self.get_module(only_name=False)
  self.format_module(_module)


def format_module(self, module):

  _type, _para, _body = module

  print("INFO [pretty] Formatting \"%s\"" % _type)
  #print(_type)
  #print(_para)
  #print(_body)

  self.fm_mod_parameters(_para)
  self.fm_mod_body(_body)

# ------------------------------------------------------------------------------
# Formats the parameter section of a module:
# 1. Assumes that each parameter is declared "parameter", i.e., no
#    multi-declaration.
# 2. Custom types must not be used.
# 3. Logic is used and not bit.
# 4. No multi-line comment after a parameter is stared and finished, but between
#    on a separate row is okay.
# 5. String parameter cannot have the type "string" and thus the found type
#    will be considered invalid.
# ------------------------------------------------------------------------------
def fm_mod_parameters(self, para):

  def skip_row(para):
    _s = para.find('\n')
    if _s >= 0:
      para = para[_s+1:].strip() # Strip so that first character is NOT a space
    else:
      para = ""

    return para

  def row_has_equal_sign(row):

    e_valid_declaration = r'[\s\w_^\-+*[\]\/$().:]*'
    e_valid_assignment  = r'[ \w_^,\-+*[\]\/\"\'()$%`<>|&!~#.?{}:]*\n'
    e0 = r'^' + e_valid_declaration + r'=' + e_valid_assignment
    match = re.search(e0, _para)
    if match:
      return True
    return False

  _f    = ""
  _para = para.strip()
  _plen = len(_para)


  # We analyse the string and reduce the remainder after each iteration
  _p_nr = 0
  while _plen != 0:

    # Starts with comment?
    if _para[0] == "/":

      # One line comment, i.e., "//"?
      if _para[1] == "/":
        _j = _para.find('\n')
      # Multi-line comment, i.e., "/*"
      else:
        _j = _para.find('*/') + 2

      # Append the comment and shift the parameter string
      _f    += self.rules.comment_head*'\n' + _para[0 : _j]
      _para  = _para[_j:].strip()
      _plen = len(_para)
      continue

    # Parameter?

    # This expression allows us to extract "parameter <type>"
    e0    = r'^parameter\s+(\w*)'
    match = re.search(e0, _para)


    # There was no comment so this MUST match
    if not match:
      # If there was no match we skip this line
      print("ERROR [fm_mod_parameters] Error 0")
      _para = skip_row(_para)
      _plen = len(_para)
      continue


    # Parameters must have a type
    _type = match.group(1)
    if not _type in sv_keywords.sv_keywords:
      # TODO: It can be a string and this keyword must be missing because parameters are
      #       not supported by tools to have a string type
      print("ERROR [fm_mod_parameters] Parameter type (%s) is not valid" % _type)
      _para = skip_row(_para)
      _plen = len(_para)
      continue

    # Checking if this row does NOT assign the parameter, i.e., uses the '=' operator
    if not row_has_equal_sign:
      print("ERROR [fm_mod_parameters] Parameter (%s) has no assign operator (=)" % _type)
      _para = skip_row(_para)
      _plen = len(_para)
      continue

    # Separating the declaration and the assignment
    _para_split =  _para.split('=')

    # Extracting the declaration
    _declaration = _para_split[0].replace("parameter",'').strip()

    # If type is logic we get all the brackets
    _fbrackets = ""
    if _type == "logic":
      _brackets = self.get_all_brackets(_declaration)
      if _brackets:
        _name = _declaration.split(']')[-1]
        _fbrackets = self.f_brackets(_brackets)

      else:
        _name = _declaration.replace("logic", '').strip()

    _para = skip_row(_para)
    _plen = len(_para)

    # --------------------------------------------------------------------------
    # Extracting a possible following comment, then find the assigned value
    # --------------------------------------------------------------------------

    # The string following the declaration part until the first newline
    _line = _para_split[1].split('\n')[0]

    # Locate a line comment
    if _line.find("//") >= 0:
      _i = _line.find("//")
      _value   = _line[:_i]
      _comment = _line[_i:]

    # Multi-line comment
    elif _line.find("/*") >= 0:
      _i = _line.find("/*")
      _value   = _line[:_i]
      _comment = self.get_subseq_multi_line_comment(_line[_i:])

    # No comment
    else:
      _value   = _line
      _comment = ""

    if self.verbosity >= 1000:
      print("Parameter: %d" % _p_nr)
      print("Type:      %s" % (_type + _fbrackets))
      print("Value:     %s" % _value)
      print("Comment:   %s" % _comment)

    _p_nr += 1


# ------------------------------------------------------------------------------
# Formats the body section of a module:
# 1.
# ------------------------------------------------------------------------------
def fm_mod_body(self, body):

  def skip_row(__b):
    _s = __b.find('\n')
    if _s >= 0:
      print("Removing: >" + __b[:_s] + "<")
      __b = __b[_s:].strip() # Strip so that first character is NOT a space
    else:
      print("Removing: >" + __b + "<")
      __b = ""

    return __b

  _f    = ""
  _body = body.strip()
  _blen = len(_body)

  print("BODY")
  print(_body)

  # while _blen != 0:
  #   _s = _body.find('\n')
  #   if _s >= 0:
  #     print(_body[:_s])
  #     _body = _body[_s+1:].strip() # Strip so that first character is NOT a space
  #   else:
  #     _body = ""
  #   _blen = len(_body)

  # print("DONE")
  # return

  # We analyse the string and reduce the remainder after each iteration
  _p_nr = 0
  while _blen != 0:

    _p_nr += 1

    # Starts with comment?
    if _body[0] == "/":
      print("%d COMMENT" % _p_nr)

      # One line comment, i.e., "//"?
      if _body[1] == "/":
        _j = _body.find('\n')
      # Multi-line comment, i.e., "/*"
      else:
        _j = _body.find('*/') + 2

      # Append the comment and shift the parameter string
      #_f    += self.rules.comment_head*'\n' + _body[0 : _j]
      print(">" + _body[:_j] + "<")
      _body  = _body[_j:].strip()
      _blen  = len(_body)
      continue


    # Input port
    match = re.search(r'^input\s+(\w*)', _body)
    if match:
      print("%d INPUT" % _p_nr)
      _body = skip_row(_body)
      _blen = len(_body)
      continue


    # Output port
    match = re.search(r'^output\s+(\w*)', _body)
    if match:
      print("%d OUTPUT" % _p_nr)
      _body = skip_row(_body)
      _blen = len(_body)
      continue


    # Only left now is interface
    print("%d INTERFACE" % _p_nr)
    _body = skip_row(_body)
    _blen = len(_body)
    continue


