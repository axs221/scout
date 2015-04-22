#!/usr/bin/python
import sys

class ParametersManager(object):
    def __init__(self):
        self.search_term = ""
        if len(sys.argv) > 1:
            self.search_term = sys.argv[1]
