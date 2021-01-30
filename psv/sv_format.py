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
  self._p.info("pretty", ("Formatting \"%s\"" % _type))

  #print(_type)
  #print(_para)
  #print(_body)

  #self.fm_mod_parameters(_para)
  self.p_mod_body(_body)

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
      self._p.error("fm_mod_parameters", "Error 0")
      _para = skip_row(_para)
      _plen = len(_para)
      continue


    # Parameters must have a type
    _type = match.group(1)
    if not _type in sv_keywords.sv_keywords:
      # TODO: It can be a string and this keyword must be missing because parameters are
      #       not supported by tools to have a string type
      self._p.error("fm_mod_parameters", ("Parameter type (%s) is not valid" % _type))
      _para = skip_row(_para)
      _plen = len(_para)
      continue

    # Checking if this row does NOT assign the parameter, i.e., uses the '=' operator
    if not row_has_equal_sign:
      self._p.error("fm_mod_parameters", ("Parameter (%s) has no assign operator (=)" % _type))
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
# Parses the body section of a module and stores the components in a list of
# lists.
# ------------------------------------------------------------------------------
def p_mod_body(self, _body):


  # A template for storing the body information. We will use "io" also for
  # defining entries as (only) row comments which should be align to the left
  # unlike comments appended to a declaration on a row, which should be column
  # aligned with eachother.
  _row_template = {"io":"", "type":"", "brackets":"", "name":"", "comment":""}

  self.bad_comments = []

  _blen = len(_body)
  _rows = []
  _row  = []
  _i = 0
  while _i != _blen:

    if _i > _blen:
      self._p.warning("p_mod_body", "Counter higher than the length")
      break

    _c = _body[_i]

    if _c == ' ' or _c == '\n':
      _i += 1
      continue

    #_in_txt = "%d/%d" % (_i, _blen)
    #input()

    if _c == '/':
      _comment = self.p_comment(_body[_i:])
      _i += len(_comment)
      _row.append(_comment)
      print(_comment)
      continue

    if _c == '[':
      _bracket = self.p_bracket(_body[_i:])
      _row.append(_bracket)
      _i += len(_bracket)
      print(_bracket)
      continue

    if _c == '$':
      _function = self.p_function(_body[_i:])
      _row.append(_function)
      _i += len(_function)
      print(_function)
      continue

    if _c == '=':
      _assign = self.p_assingment(_body[_i:])
      _row.append(_assign)
      _i += len(_assign)
      print(_assign)
      continue

    if _c == ',':
      _i += 1
      _rows.append(_row)
      _row = []
      continue

    if _c == ')':
      _i += 1
      _rows.append(_row)
      self._p.info("p_mod_body", "Done. Parsed (%d/%d) characters" % (_i, _blen))
      break

    _word = self.p_word(_body[_i:])
    _row.append(_word)
    _i += len(_word)
    print(_word)


  if self.bad_comments:
    self._p.debug("Done", "Bad style comments:")
    print(self.bad_comments)

  self._p.debug("Done", "Rows:")
  for _row in _rows:
    print(' '.join(_row))


# ------------------------------------------------------------------------------
# Comments
# Argument "txt" is a string and must begin with either "//" or "/*"
# ------------------------------------------------------------------------------

def p_comment(self, txt):

  self._p.debug("p_comment", "Called")

  _type    = ""
  _comment = ""

  for _c in txt:

    if _type == "comment_line":
      _comment += _c
      if _c == '\n':
        return _comment
      continue

    if _type == "comment_mline":
      _comment += _c
      if _c == '/' and len(_comment) >= 4 and _comment[-2] == "*":
        return _comment
      continue

    if len(_comment) == 0:
      if _c == '/':
        _comment = '/'
        continue
      else:
        self._p.fatal("p_comment", "Comment error 0")
        sys.exit(1)
        return ""

    if len(_comment) == 1:
      _comment += _c
      if _c == '/':
        _type = "comment_line"
        continue
      if _c == '*':
        _type = "comment_mline"
        continue
      self._p.warning("p_comment", "Invalid comment")
      return ""

  self._p.fatal("p_comment", "Comment error 1")
  sys.exit(1)

# ------------------------------------------------------------------------------
# Words:
# input, output, wire, logic, <labels>, parameter, int, logic
# ------------------------------------------------------------------------------

def p_word(self, txt):

  #print("DEBUG [p_word] Called")

  _word_endings = [' ', ',', '[', '=', '$', ')', '\n']
  _word         = ""

  for _c in txt:

    if _c in _word_endings:
      return _word

    _word += _c

    # Comment?
    if _c == '/':
      if _word[-1] == '/':
        _l_cmt  = self.p_comment(txt[len(_word):])
      if _word[-1] == '*':
        _ml_cmt = self.p_comment(txt[len(_word):])

  self._p.fatal("p_word", "Word error")
  sys.exit(1)

# ------------------------------------------------------------------------------
# Brackets
# ------------------------------------------------------------------------------

def p_bracket(self, txt):

  #print("DEBUG [p_bracket] Called")

  _bracket = ""
  _tlen    = len(txt)
  _i       = 0

  while _i != _tlen:

    if _i > _tlen:
      self._p.fatal("p_bracket", "Counter higher than the length")
      sys.exit(1)
      break

    _c = txt[_i]

    if _c == '$':
      _function = self.p_function(txt[_i:])
      _bracket += _function
      _i += len(_function)
      continue

    if _c == ']':
      _bracket += _c
      return _bracket

    if _c == '/':
      if txt[_i+1] == '/' or txt[_i+1] == '*':
        _comment = self.p_comment(txt[_i:])
        self.bad_comments.append(_comment)
        _i += len(_comment)
        _bracket += _comment
        self._p.warning("p_bracket", "Comment in bracket (%s)" %_comment)
        self._p.debug("p_bracket", txt[_i:_i+16])
        self._p.debug("p_bracket", txt[_i])
        continue

    _bracket += _c
    _i       += 1

  self._p.fatal("p_bracket", " No more characters!")
  sys.exit(1)

# ------------------------------------------------------------------------------
# Assignments (parameters only)
# ------------------------------------------------------------------------------

def p_assingment(self, txt):

  #print("DEBUG [p_assingment] Called")

  for _c in txt:

    # These characters ends a parameter declaration and assignment
    if _c == ',' or _c == ')':
      print("INFO [assign] %s" % _assign) #TODO: Done, what now?
      continue

    # Line comment?
    #TODO: Some idiot can set the ',' after the line comment
    if _c == '/':
      if _assign[-1] == '/':
        _pstate = "assign"
        _state  = "comment_line"
        _assign = _assign[:-1]
        continue

    # Multi line comment?
    if _c == '*':
      if _assign[-1] == '/':
        _pstate = "assign"
        _state  = "comment_mline"

    # Function?
    if _c == '$':
      _state  = "function"

    # Assignment value
    _assign += _c


# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

def p_function(self, txt):

  #print("DEBUG [p_function] Called")

  _function      = ""
  _l_parantheses = 0
  _r_parantheses = 0

  for _c in txt:
    _function += _c
    if _c == '(':
      _l_parantheses += 1
    if _c == ')':
      _r_parantheses += 1
    if _l_parantheses != 0:
      if _l_parantheses == _r_parantheses:
        return _function

  self._p.fatal("p_function", " No more characters!")
  sys.exit(1)