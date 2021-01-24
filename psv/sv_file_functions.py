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

import os, re
import subprocess

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def load_sv_file(self, file_path, rm_comments=True):

  if not self.file_exists(file_path):
    print("INFO [load_sv_file] File (%s) does not exist" % file_path)

  with open(file_path, 'r') as file:
    self.current_file = file_path
    self.svf          = file.read().split('\n')
    if rm_comments:
      # A flat string of the file with no comments for easy regexp-ing
      self.flat = self.remove_comments('\n'.join(self.svf))
    else:
      # Complete, for extracting and formating
      self.flat = '\n'.join(self.svf)




# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def find_rtl_folders(self, top):
  rtl_folders = []
  for root, dirs, _ in os.walk(top, topdown=False):
    for name in dirs:
      if name == "rtl":
        rtl_folders.append(os.path.join(root, name))
  return rtl_folders


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def find_sv_files(self, top, exclude_pkg = 0):
  sv_files = []
  for f in os.listdir(top):
    if f.endswith(".sv"):
      if exclude_pkg:
        if not f.endswith("_pkg.sv"):
          sv_files.append(top+'/'+f)
  return sv_files

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def is_directory(self, dir_path):
  return os.path.isdir(dir_path)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def make_directory(self, dir_path):
  os.mkdir(dir_path)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def file_exists(self, file_path):
  return os.path.isfile(file_path)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def get_git_root(self):
  return subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                           stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
def remove_comments(self, string):
  # Remove all occurrences streamed comments (/*COMMENT */) from string
  string = re.sub(re.compile(r"/\*.*?\*/",re.DOTALL), "", string)
  # Remove all occurrence single-line comments (//COMMENT\n ) from string
  string = re.sub(re.compile(r"//.*?\n" ), "", string)
  return string
