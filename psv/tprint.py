#!/usr/bin/env python3

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

from colorama import Fore, Back, Style

class tprint:

  def __init__(self):
    self.clr_info    = Fore.GREEN
    self.clr_warning = Fore.YELLOW
    self.clr_error   = Fore.RED
    self.clr_fail    = Fore.LIGHTMAGENTA_EX
    self.clr_fatal   = Fore.MAGENTA
    self.clr_debug   = Fore.CYAN


  def info(self, name, info):
    _str = "INFO [%s]" % (name)
    print(f"{self.clr_info}%s " % _str + Style.RESET_ALL + info)


  def warning(self, name, warning):
    _str = "WARNING [%s]" % (name)
    print(f"{self.clr_warning}%s " % _str + Style.RESET_ALL + warning)


  def error(self, name, error):
    _str = "ERROR [%s]" % (name)
    print(f"{self.clr_error}%s " % _str + Style.RESET_ALL + error)


  def fail(self, name, fail):
    _str = "FAIL [%s]" % (name)
    print(f"{self.clr_fail}%s " % _str + Style.RESET_ALL + fail)


  def fatal(self, name, fatal):
    _str = "FATAL [%s]" % (name)
    print(f"{self.clr_fatal}%s " % _str + Style.RESET_ALL + fatal)


  def debug(self, name, debug):
    _str = "DEBUG [%s]" % (name)
    print(f"{self.clr_debug}%s " % _str + Style.RESET_ALL + debug)


  def _test(self):
    self.info("__init__",    "INFO")
    self.warning("__init__", "WARNING")
    self.error("__init__",   "ERROR")
    self.fail("__init__",    "FAIL")
    self.fatal("__init__",   "FATAL")