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

        super(SearchResultsView, self).__init__(parameters_manager, view_manager, content)

    def out(self, s):
        self.view_manager.header.set_text(str(s))

    def get(self):
        search_term = self.parameters_manager.search_term  # Note that search_term may be empty
        command = "/bin/grep '" + search_term + "' %s -R" % os.getcwd()
        searchResults = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
        print command
        lines = searchResults.split('\n')
        builder = SearchResultsLinesBuilder()
        [ builder.add_line(line) for line in lines ]
        return builder.build()

    def on_keypress(self, input):
        if input in ('/', '?'):
            self.view_manager.footer.clear()
            self.view_manager.main_frame.focus_part = 'footer'
        elif input == 'enter':
            if self.view_manager.main_frame.focus_part == 'footer':
                self.start_search()
            elif self.view_manager.main_frame.focus_part == 'body':
                self.run_editor()
        elif input == 'n':
            self.search_next(self.focus_position + 1)
        elif input == 'N':
            self.search_previous(self.focus_position - 1)
        else:
            super(SearchResultsView, self).on_keypress(input)

    def run_editor(self):
        current_filename = self.content[self.focus_position].filename

        command = "vim " + current_filename
        subprocess.call(["vim", current_filename])

    def start_search(self):
        self.view_manager.main_frame.focus_part = 'body'
        self.search_next(0)

    def search_next(self, starting_position):
        if starting_position > self.content or starting_position < 0:
            return

        i = starting_position
        for line in self.content[i:len(self.content) - 1]:
            if self.view_manager.footer.get_input() in line.original_widget.text:
                self.set_focus(i)
                break
            i = i + 1

    def search_previous(self, starting_position):
        if starting_position > self.content or starting_position < 0:
            return

        i = starting_position

        reversed_content = reversed(self.content[0:i+1])
        for line in reversed_content:
            if self.view_manager.footer.get_input() in line.original_widget.text:
                self.set_focus(i)
                break
            i = i - 1
