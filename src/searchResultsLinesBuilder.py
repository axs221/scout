#!/usr/bin/python
import urwid
import re

class SearchResultsLinesBuilder(object):
    def __init__(self):
        self.lines = []
        self.current_filename = ''

    def add_line(self, text):
        if self.filter_out(text):
            return

        self.parse_text(text)
        line = self.format_line(text)
        self.decorate_and_append(line)

        return self

    def decorate_and_append(self, line, decoration='normal'):
        decorated = self.decorate(line, decoration)
        decorated.filename = self.current_filename
        self.lines.append(decorated)

    def filter_out(self, text):
        if 'Binary' in text:
            return True
        return False

    def parse_text(self, text):
        filename_match = re.match('^([a-zA-Z_\/.]+):', text)
        if filename_match:
            this_filename = filename_match.group(1)
            if this_filename != self.current_filename:
                self.decorate_and_append("")
                self.decorate_and_append(this_filename, 'filename')
                self.current_filename = filename_match.group(1)

    def format_line(self, text):
        filecontents_match = re.match('^[a-zA-Z_\/.]+:\s*(.*)$', text)
        if filecontents_match:
            return filecontents_match.group(1)
        return text
        # return 'foo'

    def build(self):
        lines = self.lines
        self.lines = []
        return lines

    def decorate(self, text, decoration='normal'):
        line = urwid.Text(text)
        new_map = lambda attr: urwid.AttrMap(line, attr, 'reveal focus')
        return new_map(decoration)
