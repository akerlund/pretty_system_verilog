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

import sys, re, copy
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
  _pbody = self.p_mod_body(_body) # Returns the parsed body
  _fbody = self.f_mod_body(_pbody) # Returns the formated body

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
# Parses the body section of a module and stores the components (rows) in a list
# of tuples. The tuple entries are containing (<type>, <value>)
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
  _end   = False
  _nl    = False
  _i = 0
  while _i != _blen:

    if _i > _blen:
      self._p.warning("p_mod_body", "Counter higher than the length")
      break

    _c = _body[_i]

    if _c == ' ':
      _i += 1
      continue


    if _c == '\n':
      _i += 1
      _end = False # A port cannot be commented on the next row
      _nl  = True
      continue

    #_in_txt = "%d/%d" % (_i, _blen)
    #input()

    if _c == '/':

      _comment = self.p_comment(_body[_i:])
      _i += len(_comment)

      # The port declaration has not ended
      if not _end:
        if not _nl:
          # No newline discovered: adding the comment to current row
          # This is necessary for the corner case of the last port's declaration which can
          # have its end character ')' after a newline
          _row.append(("c", _comment))
        else:
          # This must be a comment on a separate row, e.g., "  // Clock and reset"
          _rows.append([("c", _comment)])

      # The port declaration has ended, i.e., we have seen a ',' (or a ')')
      else:
        # If there haven't been a newline, this comment belongs to the row we have appended previously
        if not _nl:
          _rows[-1].append(("c", _comment))
        else:
          # If we get here, the declaration has ended, but there is new seen newline either
          self._p.warning("p_mod_body", "Corner case 0, should not happen (%s)"%_comment)
          _rows.append([("c", _comment)])

      _end = False
      #print(_comment)
      continue

    if _c == '[':
      _end = False
      _bracket = self.p_bracket(_body[_i:])
      _row.append(("b", _bracket))
      _i += len(_bracket)
      #print(_bracket)
      continue

    if _c == '$':
      _end = False
      _function = self.p_function(_body[_i:])
      _row.append(("f", _function))
      _i += len(_function)
      #print(_function)
      continue

    if _c == '=':
      _assign = self.p_assingment(_body[_i:])
      _row.append(("a", _assign))
      _i += len(_assign)
      #print(_assign)
      continue

    if _c == ',':
      _end = True
      _i += 1
      _rows.append(_row)
      _row = []
      continue

    if _c == ')':
      _end = True
      _i += 1
      _rows.append(_row)
      self._p.info("p_mod_body", "Done. Parsed (%d/%d) characters" % (_i, _blen))
      break

    _word = self.p_word(_body[_i:])
    _row.append(("w", _word))
    _i += len(_word)
    _end = False
    _nl  = False
    #print(_word)

  # Checking the last comment
  # if len(_rows[-1]) == 1:         # If the length of the last row is one, it is only a comment
  #   _type, _value = _rows[-2][-1] # We extract the last entry of the next last row and
  #   if _type != 'c':              # If this entry is missing a comment, we should move the len(1) entry here
  #     _rows[-2].append(_rows[-1][0])
  #     _rows = _rows[:-1]


  if self.bad_comments:
    self._p.debug("Done", "Bad style comments:")
    print(self.bad_comments)

  self._p.debug("Done", "Rows:")
  _i = 0

  for _row in _rows:
    _line = ""
    for _c in _row:
      _t, _l = _c
      _line += _l + ' '
    print("Row %d:"%_i + _line)
    _line = ""
    _i += 1

  return _rows

# ------------------------------------------------------------------------------
# Comments
# Argument "txt" is a string and must begin with either "//" or "/*"
# ------------------------------------------------------------------------------

def p_comment(self, txt):

  _type    = ""
  _comment = ""

  for _c in txt:

    if _type == "comment_line":
      if _c == '\n':
        #self._p.debug("p_comment", "Line (%s)" % _comment)
        return _comment
      _comment += _c
      continue

    if _type == "comment_mline":
      _comment += _c
      if _c == '/' and len(_comment) >= 4 and _comment[-2] == "*":
        #self._p.debug("p_comment", "Multi line (%s)" % _comment)
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
# Words, e.g.,
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
# Brackets, e.g.,
# [$clog2(PARAMETER1_P)-1 : 0]
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


# ------------------------------------------------------------------------------
# Formating a parsed body
# ------------------------------------------------------------------------------

def f_mod_body(self, pbody):

  _row_template = {"io":"", "type":"", "brackets":[], "name":"", "comment":""}

  _fbody   = []
  _ind     = 4

  _i = 0

  # For all rows we have discovered stored in the parsed body variable
  for _row in pbody:

    # Only comments so far, or is a word found?
    _w_found = False
    _port    = copy.deepcopy(_row_template)

    # Iterating all entries on one row
    for _entry in _row:

      _e_type, _e_value = _entry

      if _w_found == False and _e_type == 'w':
        _w_found = True

      # Preceeding comments
      if not _w_found:
        _cr            = copy.deepcopy(_row_template) # Comment row
        _cr["io"]      = "c"
        _cr["comment"] = _e_value
        _fbody.append(_cr)
        continue

      # We absolutely need a direction (or interface)
      if _port["io"] == "":
        _port["io"] = _e_value
        continue

      # We need a type, e.g., wire or logic, and if the type is not set yet; now it is
      if _port["type"] == "":
        if _e_type == 'w':
          _port["type"] = _e_value
          continue
        else:
          _port["type"] = " "

      # Append brackets
      if _e_type == 'b':
        _port["brackets"].append(_e_value)
        continue

      # Set the port name
      if _e_type == 'w':
        _port["name"] = _e_value
        continue

      # Trailing comments
      if _e_type == 'c':
        _port["comment"] += _e_value
        continue

    # All entries checked
    _fbody.append(_port)

    print(80*'-')
    print("Row %d has length %d: %s" % (_i, len(_row), _row))
    _io       = _port["io"]
    _type     = _port["type"]
    _brackets = ' '.join(_port["brackets"])
    _name     = _port["name"]
    _comment  = _port["comment"]
    print("IO:       " + _io)
    print("TYPE:     " + _type)
    print("BRACKETS: " + _brackets)
    print("NAME:     " + _name)
    print("COMMENT:  " + _comment)
    _i += 1



  # _i = 0
  # for _port in _fbody:
  #   _io       = _port["io"]
  #   _type     = _port["type"]
  #   _brackets = ' '.join(_port["brackets"])
  #   _name     = _port["name"]
  #   _comment  = _port["comment"]
  #   print("Entry %d" % _i)
  #   print(_io)
  #   print(_type)
  #   print(_brackets)
  #   print(_name)
  #   print(_comment)
  # _i += 1



#      _line += _l + ' '
#    print("Row %d:"%_i + _line)
#    _line = ""
#    _i += 1

#  for _row in pbody:
