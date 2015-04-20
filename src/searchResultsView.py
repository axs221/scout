#!/usr/bin/python
import os
import urwid
import subprocess
from baseView import BaseView
from searchResultsLinesBuilder import SearchResultsLinesBuilder

class SearchResultsView(BaseView):

    def __init__(self, parameters_manager, view_manager):
        self.parameters_manager = parameters_manager
        self.view_manager = view_manager

        searchResults = self.get()

        content = urwid.SimpleListWalker(searchResults)
        self.content = content

        # self.selected_commit = None

        super(SearchResultsView, self).__init__(parameters_manager, view_manager, content)

    def out(self, s):
        self.view_manager.header.set_text(str(s))

    def get(self):
        filename = self.parameters_manager.filename  # Note that filename may be empty
        searchResults = subprocess.Popen(
            "/bin/grep 'scout' %s -R" % os.path.dirname(os.path.realpath(__file__))
            , shell=True, stdout=subprocess.PIPE).stdout.read()
        lines = searchResults.split('\n')
        builder = SearchResultsLinesBuilder()
        [ builder.add_line(line) for line in lines ]
        return builder.build()

    def on_keypress(self, input):
        if input == '/':
            self.view_manager.main_frame.focus_part = 'footer'
        elif input == 'enter':
            self.view_manager.main_frame.focus_part = 'body'
            i = 0
            for line in self.content:
                if self.view_manager.footer.get_input() in line.original_widget.text:
                    self.set_focus(i)
                    break
                i = i + 1
            self.view_manager.footer.clear()
        else:
            super(SearchResultsView, self).on_keypress(input)
