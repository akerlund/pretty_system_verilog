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

import os

def load_sv_file(self, file_path):
  with open(file_path, 'r') as file:
    self.current_file = file_path
    self.svf          = file.read().split('\n')
    self.flat         = ''.join(self.svf)


def find_rtl_folders(self, top):
  rtl_folders = []
  for root, dirs, _ in os.walk(top, topdown=False):
    for name in dirs:
      if name == "rtl":
        rtl_folders.append(os.path.join(root, name))
  return rtl_folders


def find_sv_files(self, top, exclude_pkg = 0):
  sv_files = []
  for f in os.listdir(top):
    if f.endswith(".sv"):
      if exclude_pkg:
        if not f.endswith("_pkg.sv"):
          sv_files.append(top+'/'+f)
  return sv_files