from __future__ import with_statement

""" various useful functions """
def file_get_contents(filename):
    with open(filename, "rb") as f:
        return f.read()

