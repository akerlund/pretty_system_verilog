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

import sys, re
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
# 1. Multi-vectors must be defined on one row only
# 2. No multi-line comment inside declarations
# 3.
# ------------------------------------------------------------------------------
def fm_mod_body(self, body):


  # A template for storing the body information. We will use "io" also for
  # defining entries as (only) row comments which should be align to the left
  # unlike comments appended to a declaration on a row, which should be column
  # aligned with eachother.
  _row_template = {"io":"", "type":"", "brackets":"", "name":"", "comment":""}

  # List for saving the parsed rows of the module
  _b_list = []

  # Before analysing, we remove any preceding spaces and check the length
  _body = body.strip()
  _blen = len(_body)

  print("BODY")
  print(_body)

  _state = "start"


  _word      = ""
  _comment   = ""
  _bracket   = ""
  _p_counter = 0  # Counting parantheses

  for _c in body:

    #print(_c, end='')

    if _state == "start":

      if _c == ' ':
        continue

      if _c == '/':
        _state   = "comment_begin"
        _comment = "/"
        continue

      if _c == '[':
        _state   = "bracket"
        _bracket = "["
        continue

      if _c == '$':
        _state    = "function"
        _function = "$"
        continue

      if _c == '=':
        _state   = "assign"
        _bracket = "["
        continue

      _state = "word"
      _word  = _c
      continue

    # --------------------------------------------------------------------------
    # Comments
    # --------------------------------------------------------------------------

    if _state == "comment_begin":

      if _c == '/':
        _state   = "comment_line"
        _comment = "//"
        continue

      if _c == '*':
        _state   = "comment_mline"
        _comment = "/*"
        continue

      print("ERROR [body_parser] /")
      sys.exit(1)

    if _state == "comment_line":

      if _c == '\n':
        _state          = "start"
        _row            = _row_template
        _row["io"]      = "comment_line"
        _row["comment"] = _comment
        continue

      _comment += _c
      continue

    if _state == "comment_mline":

      if _c == '/' and _comment[-1] == "*":
        _state          = "start"
        _row            = _row_template
        _row["io"]      = "comment_mline"
        _row["comment"] = _comment
        continue


    # --------------------------------------------------------------------------
    # Words
    # --------------------------------------------------------------------------

    if _state == "words":

      if _c == ' ':
        _state = "start"
        _word  += _c
        continue

      if _c == '[':
        _state   = "bracket"
        _bracket = "["
        # TODO: Save word
        continue

    # --------------------------------------------------------------------------
    # Brackets
    # --------------------------------------------------------------------------

    if _state == "bracket":

      if _c == ']':
        _state  = "start"
      _bracket += _c
      continue

    # --------------------------------------------------------------------------
    # Functions
    # TODO: Be inside brackets
    # --------------------------------------------------------------------------


















# def fm_mod_body_old(self, body):


#   def skip_row(__b):
#     _s = __b.find('\n')
#     if _s >= 0:
#       print("Removing: >" + __b[:_s] + "<")
#       __b = __b[_s:].strip() # Strip so that first character is NOT a space
#     else:
#       print("Removing: >" + __b + "<")
#       __b = ""

#     return __b

#   # We analyse the string and reduce the remainder (_blen) after each iteration

#   _p_nr = 0 # Iteration counter
#   while _blen != 0:

#     _p_nr += 1

#     # Variables for the parsed information
#     _io       = ""
#     _type     = ""
#     _brackets = ""
#     _name     = ""
#     _comment  = ""

#     # Starts with comment?
#     if _body[0] == "/":

#       _io = "comment"

#       print("%d COMMENT" % _p_nr)

#       # One line comment, i.e., "//"?
#       if _body[1] == "/":
#         _j = _body.find('\n')
#       # Multi-line comment, i.e., "/*"
#       else:
#         _j = _body.find('*/') + 2

#       # Append the comment and shift the parameter string
#       #_f    += self.rules.comment_head*'\n' + _body[0 : _j]
#       print(">" + _body[:_j] + "<")
#       _body  = _body[_j:].strip()
#       _blen  = len(_body)
#       print('\n')
#       continue

#     # If the port type is either input or output this variable is set to True
#     # and common code executed subsequently
#     _io_match = False

#     # Input port
#     match = re.search(r'^input\s+(\w*)', _body)
#     if match:

#       _io_match = True
#       _io       = "input"
#       _type     = match.group(1)
#       if _type != "wire":
#         print("WARNING [fm_mod_body] input port has the type (%s)" % _type)

#       print("%d INPUT" % _p_nr)
#       print("Group(1) = %s" % match.group(1))


#     # Output port
#     match = re.search(r'^output\s+(\w*)', _body)
#     if match:

#       _io_match = True
#       _io       = "output"
#       _type     = match.group(1)
#       if _type != "logic":
#         print("WARNING [fm_mod_body] output port has the type (%s)" % _type)

#       print("%d OUTPUT" % _p_nr)
#       print("Group(1) = %s" % match.group(1))


#     # Found either input or output port
#     if _io_match:

#       _line = _body.split('\n')[0]

#       # Get all brackets on this line
#       # TODO: But perhaps someone declared on multiple lines?
#       _brackets = self.get_all_brackets(_line)


#       _ci          = _line.find("//")  # Comment integer index
#       _has_comment = _ci >= 0          # Comment boolean
#       _rt          = 0                 # Set to a value by a matching regexp for knowing which matched

#       # If there is a comment, we look for the name up until the beginning of the
#       # comment because we consider the ',' which lets us know if it is the last
#       # port
#       if _has_comment:

#         if ',' in _line[:_ci]:            # Not the last port if a ',' is found
#           _e0   = r'^(\w*)\s*,\s*(//\w*)' # Regexp to extract name and comment
#           match = re.search(_e0,  _line[:_ci])
#           _rt   = 1
#         else:
#           _e0   = r'^(\w*)\s*//(\w*)'
#           match = re.search(_e0,  _line[:_ci])
#           _rt   = 2

#       else:

#         if ',' in _line:                  # Not the last port if a ',' is found
#           _e0   = r'^(\w*)\s*,' # Regexp to extract name and comment
#           match = re.search(_e0, _line)
#           _rt   = 3
#         else:
#           _e0   = r'^(\w*)\s*'
#           match = re.search(_e0, _line)
#           _rt   = 4

#         if not match:
#           print("ERROR [fm_mod_body] Error %d: %s" % (_rt, _line))
#         else:
#           _name    = match.group(1)
#           _comment = ""
#           if _rt <= 3:
#             _comment  = match.group(2)

#           print("_name    = %s" % _name)
#           print("_comment = %s" % _comment)

#       _body = skip_row(_body)
#       _blen = len(_body)

#       print('\n')

#       continue


#     # Only left now is interface, i.e., custom types?


#     _io = "custom"

#     print("%d INTERFACE" % _p_nr)
#     _body = skip_row(_body)
#     _blen = len(_body)
#     continue


