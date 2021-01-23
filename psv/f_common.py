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

# ------------------------------------------------------------------------------
# Format a list of bracket according to defined rules
# ------------------------------------------------------------------------------
def f_brackets(self, b_list):

  _f = ""
  for _bra in b_list:
    _b  = _bra.replace(' ', '')           # Remove all white spaces
    _i  = self.rules.r_bracket_spaces_in  # Look up how many spaces are configured
    _t  = _i*' ' + ':' + _i*' '           # Create the ":" separator
    _f += _b.replace(':', _t)             # Replace the old separator
    _i += self.rules.r_bracket_spaces_out # Separating spaces between brackets
    _f += _i*' '

  return _f