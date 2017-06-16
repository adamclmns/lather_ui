# Tkinter has different import names on different versions.
try:
    # Python2.7 imports
    import Tkinter
    import tkFileDialog
    import tkMessageBox
    import Tkconstants
    import ScrolledText
except ImportError:
    # Python 3.6 imports
    import tkinter as Tkinter
    from tkinter import (
        filedialog as tkFileDialog,
        messagebox as tkMessageBox,
        constants as Tkconstants,
        scrolledtext as ScrolledText,
    )
# These are all standard Libs
import subprocess
import shlex
import sys
import os

from threading import Thread
# from Queue import Queue, Empty
from time import sleep


def getFilename():
    '''this will get a filename using Tkinter browse dialog
    '''
    file_opt = options = {}
    options['filetypes'] = [('shell script', '.sh'), ('all files', '.*')]
    options['initialdir'] = os.getcwd()
    frame = Tkinter.Frame()
    options['parent'] = frame
    options['title'] = 'select a shell script source file: '
    filepath = tkFileDialog.askopenfilename(**file_opt)
    frame.destroy()
    return filepath


def writeFile(filename, content, content_header=""):
    '''this writes some given content to a given filename in binary append mode
    '''
    # wb - write binary, truncates file before writing
    # ab - append binary
    # binary will keep original line endings, and not make the file look ugly in notepad++
    outFile = open(filename, 'ab')
    # TODO: Handle Exceptions
    outFile.write(content_header + '\n')
    outFile.write(content + '\n')
    outFile.close()


def get_file_options():
    options = {}
    options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
    options['initialdir'] = os.getcwd()
    options['parent'] = self.root
    options['title'] = 'select a jmx file: '


class RedirectText(object):
    """Helper class to redirect STD Out to a particular UI element"""

    def __init__(self, text_ctrl):
        """Constructor"""
        self.output = text_ctrl
        self.fileno = sys.stdout.fileno

    def write(self, string):
        """ write to the redirected terminal"""
        self.output.insert(Tkinter.INSERT, string + "\n")


class AbstractWindow(Tkinter.Frame):

    def userAlert(self, message):
        tkMessageBox.showinfo("Alert:", message)

    def restart(self):
        subprocess.Popen('python App.py', shell=True)
        self.root.quit()

    def hello(self):
        tkMessageBox.showinfo("INFO:", "This feature is not implemented yet")
