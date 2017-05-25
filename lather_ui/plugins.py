import os, json
try:
    import tkinter as Tkinter
except:
    import Tkinter

class LatherPluginConfigForm(Tkinter.Frame):
    
    def __init__(self, properties_to_prompt):
        # Dynamically build a form for the plugin's config property values. 
        self.form_data = self._build_form(properties_to_prompt)
        self.root = Tkinter.Toplevel()
    def _build_form(self, properties):
        frame = Tkinter.Frame()
        form_data = {}
        for prop in properties:
            form_data[prop] = Tkinter.StringVar()
            Tkinter.Label(frame, text=prop).pack()
            Tkinter.Entry(frame, textvariable=form_data[prop]).pack()
        Tkinter.Button(frame, text="SUBMIT", command=self._submit_form).pack()

    def _submit_form(self):
        for prop in self.form_data.keys():
            self.form_data[prop] = self.form_data[prop].get()
        self.root.destroy()
        return self.form_data

class AbstractLatherPlugin():
    def __init__(self, name, plugin_menu):
        self._name = name
        self._config_properties = []
        self._config_file_path = os.path.dirname(os.path.realpath(__file__)) + "\\plugin-config\\" + name +".json"  # Config is saved to JSON file in a directory 
        self._config = self._read_config()
        self._plugin_menu = plugin_menu # This is for adding Menus to the window for the plugin.

    def beforeRequest(self, client):
        # Optional - Implementation in Concrete Plugin
        pass

    def afterRequest(self, client):
        # Optional - Implementation in Concrete Plugin
        pass

    def onClientCreation(self, client):
        # Optional - Implementation in Concrete Plugin
        pass

    def afterResponse(self, client):
        pass

    def _add_plugin_menu(self):
        pass

    def _prompt_config(self):
        my_config = LatherPluginConfigForm(self._config_properties)
        # TODO: THink about the following...
        #   Read config from file?
        #   Write Config to File?
        print()
        pass

    def _read_config(self):
        try:
            with open(self._config_file_path) as config:
                return json.loads(config.read())
        except:
            print("Config file not found... or other error happened")
            return

    
    def _write_config(self, config_to_write):
        try:
            with open(self._config_file_path) as config:
                config.write(json.dumps(config_to_write))
            return True
        except:
            return False

class SimpleHTTPHeaderPlugin(AbstractLatherPlugin):
    def __init__(self):
        # Build the plugin object, and implement the methods you need.... ignore the ones you don't. 
        _name = "HTTTP-Header-Plugin"
        AbstractLatherPlugin.__init__(self, _name)
        self._config_properties = ["Http-Headers"]

    def beforeRequest(self, client):
        # Create and add Headers to HTTP afterRequest
        client.set_options(headers=self._config['Http-Headers'])

