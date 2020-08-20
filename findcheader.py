#!python3

import os
import re
import sys

if len(sys.argv) < 2:
    print(r"Error, no input file.")
    exit()
    
filename = sys.argv[1]
    
if not os.path.isfile(filename):
    exit()

std_headers = [r"<assert.h>", r"<complex.h>", r"ctype.h", r"<errno.h>",
               r"<fenv.h>", r"<float.h>", r"<inttypes.h>", r"<iso646.h>",
               r"<limits.h>", r"<locale.h>", r"<math.h>", r"<setjmp.h>",
               r"<signal.h>", r"<stdalign.h>", r"<stdarg.h>", r"<stdatomic.h>",
               r"<stdbool.h>", r"<stddef.h>", r"<stdint.h>", r"<stdio.h>",
               r"<stdlib.h>", r"<stdnoreturn.h>", r"<string.h>", r"<tgmath.h>",
               r"<threads.h>", r"<time.h>", r"<uchar.h>", r"<wchar.h>",
               r"<wctype.h>"]

standard = []
suspicious = []

def location_in_file(filename, header):
    with open(filename) as infile:
        for (line_num, line) in enumerate(infile.readlines()):
            loc = line.find(header)
            if loc >= 0:
                return (line_num+1, loc)

with open(filename, 'r') as infile:
    headers = re.findall(r"<.*\.h>", infile.read())
    for header in headers:
        if header in std_headers:
            standard.append(header)
        else:
            suspicious.append(header)
            
def print_header_warning(header, warning):
    (line_num, location) = location_in_file(filename, header)
    print(r"{filename}:{line}:{location} warning: {warning} '{header}'".format(filename=filename, line=line_num, location=location, warning=warning, header=header))
            
if standard:
    for header in standard:
        print_header_warning(header, r"Use of C-header")
    
if suspicious:
    for header in suspicious:
        print_header_warning(header, r"Use of suspicous header (might be C)")
