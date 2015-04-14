#!/usr/bin/python
import os
import urwid
import subprocess
from baseView import BaseView
from searchResultsLinesBuilder import SearchResultsLinesBuilder

class SearchResultsView(BaseView):

    def __init__(self, parameters_manager, view_manager):
        self.parameters_manager = parameters_manager

        searchResults = self.get()

        content = urwid.SimpleListWalker(searchResults)
        self.content = content

        self.selected_commit = None

        super(SearchResultsView, self).__init__(parameters_manager, view_manager, content)

    def out(self, s):
        self.show_key.set_text(str(s))

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
        if input == 'h':
            self.add_to_diff(input)
        if input == 'enter':
            self.add_to_diff(input)
        elif input == 'c':
            show_key = self.view_manager.current_view.show_key
            self.selected_commit = None
            show_key.set_text("Press any key")
        else:
            super(SearchResultsView, self).on_keypress(input)

    def add_to_diff(self, input):
        if self.selected_commit or input == 'h':
            listbox = None

            if input == 'h':
                previously_selected_commit = 'HEAD'
                newly_selected_commit = None
            else:
                previously_selected_commit = self.selected_commit
                newly_selected_commit = self.content[self.focus_position].commit

            self.show_diff(previously_selected_commit, newly_selected_commit)
        else:
            show_key = self.view_manager.current_view.show_key
            self.selected_commit = self.content[self.focus_position].commit
            show_key.set_text("Press enter on another commit, or enter here again to compare to HEAD\nCommit: " + self.selected_commit)

    def show_diff(self, before_commit, after_commit):
        pass
        # if before_commit == after_commit:
        #     listbox = DiffView(self.parameters_manager, self.view_manager, after_commit, 'HEAD')
        # else:
        #     listbox = DiffView(self.parameters_manager, self.view_manager, before_commit, after_commit)

        # self.view_manager.change_view(listbox)
