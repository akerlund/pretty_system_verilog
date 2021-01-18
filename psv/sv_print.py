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
#
# ------------------------------------------------------------------------------
def print_all_modules(self, print_sub=True, table=False):

  print(80*'-')
  print("- All (%d) modules" % len(self.all_modules))
  print(80*'-')

  _sorted = []

  # Print a sorted table
  if table:

    _longest = 0

    for _m in self.all_modules.keys():
      _sorted.append(_m)
      if len(_m) > _longest:
        _longest = len(_m)

    _sorted.sort()
    _i = 0
    _table = ""

    for _s in _sorted:
      _table += ('\''+_s+'\'').ljust(_longest+1+2)
      if _i == 3:
        _i = 0
        _table += '\n'
      else:
        _i += 1

    print(_table)

  else:

    for _m in self.all_modules.keys():
      _sorted.append(_m)

    _sorted.sort()
    _colon = ":" if print_sub else ""

    for key in _sorted:
      sub = self.all_modules[key]
      print(key + _colon)
      if print_sub:
        if not len(sub):
          print("  - No submodules")
        else:
          for module_type, _ in sub:
            print("  " + module_type)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def print_top_modules(self):

  print(80*'-')
  print("- All (%d) tops" % len(self.tops))
  print(80*'-')
  for t in self.tops:
    print(t)

  print("\n\n")
  print(80*'-')
  print("- All (%d) non-tops" % len(self.tops_n))
  print(80*'-')
  for t in self.tops_n:
    print(t)