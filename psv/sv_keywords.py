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
# To improve performance, the most commonly found (or believed to be found)
# keywords are put first in the list
# ------------------------------------------------------------------------------
sv_keywords = [
# Common
"module",
"if",
"task",
"begin",
"always_ff",
"always_comb",
# Possible
"bit",
"break",
"const",
"default",
"endcase",
"endtask",
"enum",
"for",
"foreach",
"forever",
"fork",
"forkjoin",
"function",
"generate",
"iff",
"import",
"incdir",
"include",
"input",
"int",
"interface",
"localparam",
"logic",
"or",
"property",
"signed",
"wire",
"with",
# Not decided or uncommon
"alias",
"always",
"always_latch",
"and",
"assert",
"assign",
"assume",
"automatic",
"before",
"bind",
"bins",
"binsof",
"buf",
"bufif0",
"bufif1",
"byte",
"case",
"casex",
"casez",
"cell",
"chandle",
"class",
"clocking",
"cmos",
"config",
"constraint",
"context",
"continue",
"cover",
"covergroup",
"coverpoint",
"cross",
"deassign",
"defparam",
"design",
"disable",
"dist",
"do",
"edge",
"else",
"end",
"endclass",
"endclocking",
"endconfig",
"endfunction",
"endgenerate",
"endgroup",
"endinterface",
"endmodule",
"endpackage",
"endprimitive",
"endprogram",
"endproperty",
"endspecify",
"endsequence",
"endtable",
"event",
"expect",
"export",
"extends",
"extern",
"final",
"first_match",
"force",
"genvar",
"highz0",
"highz1",
"ifnone",
"ignore_bins",
"illegal_bins",
"initial",
"inout",
"inside",
"instance",
"integer",
"intersect",
"join",
"join_any",
"join_none",
"large",
"liblist",
"library",
"local",
"longint",
"macromodule",
"matches",
"medium",
"modport",
"nand",
"negedge",
"new",
"nmos",
"nor",
"noshowcancelled",
"not",
"notif0",
"notif1",
"null",
"output",
"package",
"packed",
"parameter",
"pmos",
"posedge",
"primitive",
"priority",
"program",
"protected",
"pull0",
"pull1",
"pulldown",
"pullup",
"pulsestyle_onevent",
"pulsestyle_ondetect",
"pure",
"rand",
"randc",
"randcase",
"randsequence",
"rcmos",
"real",
"realtime",
"ref",
"reg",
"release",
"repeat",
"return",
"rnmos",
"rpmos",
"rtran",
"rtranif0",
"rtranif1",
"scalared",
"sequence",
"shortint",
"shortreal",
"showcancelled",
"small",
"solve",
"specify",
"specparam",
"static",
"string",
"strong0",
"strong1",
"struct",
"super",
"supply0",
"supply1",
"table",
"tagged",
"this",
"throughout",
"time",
"timeprecision",
"timeunit",
"tran",
"tranif0",
"tranif1",
"tri",
"tri0",
"tri1",
"triand",
"trior",
"trireg",
"type",
"typedef",
"union",
"unique",
"unsigned",
"use",
"uwire",
"var",
"vectored",
"virtual",
"void",
"wait",
"wait_order",
"wand",
"weak0",
"weak1",
"while",
"wildcard",
"within",
"wor",
"xnor",
"xor"]