from __future__ import unicode_literals, print_function, division, absolute_import

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

import logging
import sys
import os

from .lather_client import SudsClientWrapper
from .helpers import AbstractWindow, RedirectText


class XMLFormWindow(AbstractWindow):
    # Will dynamically create a form based on SUDS request definition (with datepickers and stuff, eventually...)
    def __init__(self, callback, method):
        self.root = Tkinter.Toplevel()
        self.frame = Tkinter.Frame(self.root)
        self.callback = callback
        self.method = method
        self.param_stringVars = {}
        self.param_infos = {}
        self.method_signature = None

    def buildForm(self, method_signature):
        method_params = method_signature['params']
        self.method_signature = method_signature
        print("BUILDING FORM....", end="")
        print(method_signature)
        frame = Tkinter.Frame(self.root)
        for param_key in method_params:
            param = param_key.split(' ')
            if param[0].split(':')[0] == "xs":
                Tkinter.Label(frame, text=param_key).pack()
                self.param_stringVars[param_key] = Tkinter.StringVar()
                Tkinter.Entry(frame, textvariable=self.param_stringVars[param_key], width=60).pack()
            else:
                Tkinter.Label(
                    frame,
                    text="This is a complex element... not yet supported. type is {}".format(param_key)
                ).pack()
            frame.pack()

        Tkinter.Button(frame, text="SUBMIT", command=self.submitForm).pack()

    def pack_StringVarToStrings(self, param_stringVars):
        """ get raw string types from StrinVars """
        packed_params = {}
        for param_key in param_stringVars.keys():
            packed_params[param_key] = param_stringVars[param_key].get()
        return packed_params

    def pack_removeEmptyStrings(self, param_stringVars):
        """ Remove Empty Parameters from the Dictionary """
        packed_params = {}
        for param_key in param_stringVars.keys():
            if self.param_stringVars[param_key].get() is not "":
                packed_params[param_key] = self.param_stringVars[param_key]
        return packed_params

    def submitForm(self):
        call_params = {}
        call_params = self.pack_removeEmptyStrings(self.param_stringVars)
        call_params = self.pack_StringVarToStrings(call_params)
        self.callback(self.method, call_params)
        self.root.destroy()


class MainWindow(Tkinter.Tk):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.soap_client = None
        self.file_opt = options = {}
        self.frame = Tkinter.Frame(self)
        self.frame.pack()
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # define buttons and labels and fields
        self.current_url = Tkinter.StringVar()
        self.current_url.set('http://www.webservicex.com/globalweather.asmx?WSDL')
        button_style = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        # This is actually legit...
        self.buttonFrame = leftFrame = Tkinter.Frame()
        # there will be buttons here some day...
        self.disposableFrame = disposableFrame = Tkinter.Frame()
        self.generate_Type_lbl = Tkinter.Label(disposableFrame, text="GENERATE TYPES:")
        self.generate_Type_lbl.pack()
        leftFrame.pack(side="left", fill="y")

        self.topFrame = topFrame = Tkinter.Frame()
        self.url_field = Tkinter.Entry(topFrame, textvariable=self.current_url, width=180)
        self.url_field.pack(side="left", fill="both")
        self.get_wsdl_btn = Tkinter.Button(topFrame, text='Get WSDL', command=self.get_wsdl).pack(side="left")
        topFrame.pack(fill="both")

        self.middleFrame = middleFrame = Tkinter.Frame()
        # Left Console for outgoing XML
        self.console_left = ScrolledText.ScrolledText(middleFrame)
        self.console_left.pack(side="left", fill="y")
        self.re_left = RedirectText(self.console_left)
        # Right Console for Incoming XML
        self.console_right = ScrolledText.ScrolledText(middleFrame)
        self.console_right.pack(side="right", fill="y")
        self.re_right = RedirectText(self.console_right)
        middleFrame.pack()

        self.bottomFrame = bottomFrame = Tkinter.Frame()
        # Bottom Console for general logging output
        self.console_bottom = ScrolledText.ScrolledText(bottomFrame)
        self.console_bottom.pack(side='left', fill="both", expand=True)
        self.re_bottom = RedirectText(self.console_bottom)
        sys.stdout = self.re_bottom
        bottomFrame.pack(fill="both")

        # FOR LAYOUT DEBUGGING
        self.re_left.write("LEFT CONSOLE")
        self.re_right.write("RIGHT CONSOLE")
        self.re_bottom.write("BOTTOM CONSOLE")
        # END LAYOUT DEBUGGING

        # define options for opening or saving a file
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = os.getcwd()
        options['parent'] = self
        options['title'] = 'select a file: '

        # Define the Menu bar
        menubar = Tkinter.Menu(self)
        filemenu = Tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="", command=self.hello)
        filemenu.add_command(label="Save", command=self.hello)
        filemenu.add_separator()
        # filemenu.add_command(label="Restart pyJmx", command=self.restart)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        runMenu = Tkinter.Menu(menubar, tearoff=0)
        runMenu.add_command(label="Jmeter GUI", command=self.hello)
        runMenu.add_command(label="JMX Test via Console", command=self.hello)
        runMenu.add_command(label="run Selected JMX", command=self.hello)
        menubar.add_cascade(label="Run...", menu=runMenu)

        plugin_menu = Tkinter.Menu(menubar, tearoff=0)

        # Add Plugin Menu items here
        # TODO: Register plugin menus
        # TODO: For each plugin, add the plugin submenu (if any)
        menubar.add_cascade(labe="Plugins", menu=plugin_menu)
        self.config(menu=menubar)

        self.title("SUDS UI v0.0.01-SNAPSHOT - SoapUI Alternative in Python/Legacy Python")

    def hello(self):
        tkMessageBox.showinfo("INFO:", "This feature is not implemented yet")

    def run(self):
        self.mainloop()

    def get_wsdl(self):
        url = self.current_url.get()
        self.soap_client = SudsClientWrapper(url)
        self.build_operation_buttons()

    def build_operation_buttons(self):

        self.disposableFrame.destroy()
        # This is actually legit...
        self.disposableFrame = disposableFrame = Tkinter.Frame(self.buttonFrame)
        self.generate_Type_lbl = Tkinter.Label(disposableFrame, text="GENERATE TYPES:")
        self.generate_Type_lbl.pack()
        disposableFrame.pack(side="left", fill="y")
        services = self.soap_client.auto_discovered_services
        print(services)
        for s in services.keys():
            Tkinter.Label(disposableFrame, text=s).pack()
            for p in services[s]['ports'].keys():
                Tkinter.Label(disposableFrame, text=p).pack()
                for m in services[s]['ports'][p]['methods'].keys():
                    print("Creating button with parameters for createMessage: ", end="")
                    print(s, p, m)
                    Tkinter.Button(
                        self.disposableFrame,
                        text=m,
                        command=self.mk_button_callback(s, p, m)
                    ).pack()

    def mk_button_callback(self, s, p, m):
        def createMessage():
            print("Requesting: ", end="")
            print(s, p, m)
            # sig = self.soap_client.getMethodSignature2(m)

            sig = self.soap_client.getMethodSignature(s, p, m)

            form = XMLFormWindow(self.XMLFormCallback, m)
            form.buildForm(sig)
            form.root.mainloop()
        return createMessage

    def XMLFormCallback(self, method, parameters):
        try:
            self.soap_client.sendCall(method, parameters)
        except Exception as ex:
            logging.exception(ex)
        self.re_left.write(str(self.soap_client.getXMLRequest()))
        self.re_right.write(str(self.soap_client.getXMLResponse()))


def main():
    MainWindow().run()


if __name__ == '__main__':
    main()
