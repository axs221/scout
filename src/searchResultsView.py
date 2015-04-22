#!/usr/bin/python
import logging
import os
import urwid
import subprocess
from baseView import BaseView
from searchResultsLinesBuilder import SearchResultsLinesBuilder

class SearchResultsView(BaseView):

    def __init__(self, parameters_manager, view_manager):
        LOG_FILENAME = 'logging_example.out'
        logging.basicConfig(filename=LOG_FILENAME,
                            level=logging.DEBUG,
                            )
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
        if input in ('/', '?'):
            self.view_manager.footer.clear()
            self.view_manager.main_frame.focus_part = 'footer'
        elif input == 'enter':
            self.start_search()
        elif input == 'n':
            self.search_next(self.focus_position + 1)
        elif input == 'N':
            self.search_previous(self.focus_position - 1)
        else:
            super(SearchResultsView, self).on_keypress(input)

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
        logging.info('Starting from: %s' % starting_position)

        reversed_content = self.content[0:i+1][::-1]
        for line in reversed_content:
            logging.info('Line number: %s' % i)
            logging.info('Line: %s' % line.original_widget.text)
            if self.view_manager.footer.get_input() in line.original_widget.text:
                self.set_focus(i)
                break
            i = i - 1
