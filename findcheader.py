#!python3
"""findcheader will find uses of C headers in C++ code files."""

import os
import re
import sys

std_headers = [r"<assert.h>", r"<complex.h>", r"ctype.h", r"<errno.h>",
               r"<fenv.h>", r"<float.h>", r"<inttypes.h>", r"<iso646.h>",
               r"<limits.h>", r"<locale.h>", r"<math.h>", r"<setjmp.h>",
               r"<signal.h>", r"<stdalign.h>", r"<stdarg.h>", r"<stdatomic.h>",
               r"<stdbool.h>", r"<stddef.h>", r"<stdint.h>", r"<stdio.h>",
               r"<stdlib.h>", r"<stdnoreturn.h>", r"<string.h>", r"<tgmath.h>",
               r"<threads.h>", r"<time.h>", r"<uchar.h>", r"<wchar.h>",
               r"<wctype.h>"]


def find_headers(filename: str) -> [str]:
    """Finds potential interesting headers in a file."""
    with open(filename, 'r') as infile:
        found_headers = re.findall(r"<.*\.h>", infile.read())
    return found_headers


def location_in_file(filename: str, header_str: str) -> (int, int):
    """Determines the usage location of a specified header in a file."""
    with open(filename) as infile:
        for (line_num, line) in enumerate(infile.readlines()):
            loc = line.find(header_str)
            if loc >= 0:
                return line_num + 1, loc
    return None


def print_header_warning(filename: str, header_str: str, warning: str):
    """Print a warning line for a header usage"""
    (line_num, location) = location_in_file(filename, header_str)
    print(r"{filename}:{line}:{location} warning: {warning} '{header}'".format(
        filename=filename, line=line_num, location=location, warning=warning, header=header_str))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(r"Error, no input file.")
        sys.exit()

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        sys.exit()

    standard = []
    suspicious = []

    headers = find_headers(input_file)
    for header in headers:
        if header in std_headers:
            standard.append(header)
        else:
            suspicious.append(header)

    if standard:
        for header in standard:
            print_header_warning(input_file, header, r"Use of C-header")

    if suspicious:
        for header in suspicious:
            print_header_warning(input_file, header, r"Use of suspicious header (might be C)")
