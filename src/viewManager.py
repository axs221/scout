#!/usr/bin/python
import urwid
from Queue import LifoQueue

class ViewManager(object):
    def __init__(self):
        self.main_frame = None
        self.current_view = None
        self.last_view_stack = LifoQueue()
        self.header = None
        self.footer = None

    def start(self):
        self._loop = urwid.MainLoop(self.main_frame, self.get_pallette(), unhandled_input=self.on_keypress)
        self._loop.run()

    def change_view(self, view):
        self.last_view_stack.put(self.current_view)
        self._update_view(view)

    def close_current_view(self):
        view = self.last_view_stack.get()
        self._update_view(view)

    def initialize_frame(self, view):
        self.header = urwid.AttrMap(urwid.Text("Press any key", wrap='clip'), 'header')
        self.footer = SearchBar()
        self.main_frame = urwid.Frame(view, self.header, self.footer.control, focus_part='body')

    def _update_view(self, view):
        self.current_view = view
        self.main_frame.contents['body'] = ( view, None )
        self._loop.draw_screen()

    def on_keypress(self, input):
        self.current_view.on_keypress(input)

    def get_pallette(self):
        palette = [('header', 'black', 'dark green', 'standout'),
                   ('footer', 'black', 'dark green', 'standout'),
                   ('normal', 'white', 'black'),
                   ('reveal focus', 'white', 'dark blue', 'standout'),
                   ('filename', 'light blue', 'black'),
                   ('diff', 'black', 'dark green', 'standout'),
                   ('added', 'dark green', 'black'),
                   ('deleted', 'dark red', 'black')]
        return palette

class SearchBar(object):
    def __init__(self):
        self.pretext = "Search: " 

        self._raw_control = urwid.Edit(('footer', self.pretext))
        self.control = urwid.AttrMap(self._raw_control, 'footer')

    def clear(self):
        self._raw_control.set_edit_text('')

    def get_input(self):
        return self._raw_control.edit_text
