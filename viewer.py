#!/usr/bin/env python3
# This is a HORRIBLE hack to view svg generated from pygal and to convert them to png
# The script uses a webview to properly display the svg and a window screenshot to save it as a png
# Escape / Ctrl+C / Close window to quit
# Ctrl+s to save a .png

import ntpath
import os
import signal
import sys

# GI imports
from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import WebKit2

# Check argv length
if len(sys.argv) != 2:
    print("Invalid args")
    sys.exit(0)

# Constants
FILE = os.path.abspath(sys.argv[1])
FNAME = ntpath.basename(FILE)

# Viewer window
class  Viewer:
    def __init__(self):
        global window

        # Viewer GUI
        window = Gtk.Window()
        window.set_title("viewer - " + FNAME)
        window.set_size_request(800,600)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.connect('delete-event',Gtk.main_quit)
        web = WebKit2.WebView()
        web.load_uri("file://" + FILE);
        window.connect("key-press-event", self.key_pressed)
        window.add(web)
        window.show_all()

        self.window = window

    def savepng(self):
        PNGFILE = FILE + '.png'

        ## Save png
        win = Gdk.get_default_root_window().get_screen().get_active_window()
        h = win.get_height()
        w = win.get_width()
        pb = Gdk.pixbuf_get_from_window(win, 0, 0, w, h)
        if (pb != None):
            pb.savev(PNGFILE,"png", (), ())

        ## Show alert dialog
        dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.ERROR,Gtk.ButtonsType.CLOSE, "Image exported to png:")
        dialog.format_secondary_text(PNGFILE)
        dialog.run()
        dialog.destroy()

    def key_pressed(self, widget, event):
        modifiers = Gtk.accelerator_get_default_mod_mask()
        # Save png on 'ctrl+s'
        if event.state & modifiers == Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_s:
            self.savepng()
            return True
        # Quit on 'escape'
        elif event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        return False

# Main
Viewer()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
