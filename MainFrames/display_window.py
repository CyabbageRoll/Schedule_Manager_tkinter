from collections import OrderedDict
import tkinter as tk
from tkinter import ttk

class DisplayWindow(ttk.Notebook):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.SP = master.SP
        self.SD = master.SD

        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.logger.debug("initialized Command Window")

    def set_variables(self):
        pass

    def set_init(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["Tasks"] = tk.Frame(self, bg="#ee2222")
        self.w["Projects"] = tk.Frame(self, bg="#ee4444")
        self.w["Settings"] = tk.Frame(self, bg="#ee5555")
        self.w["Follows"] = tk.Frame(self, bg="#ee5555")


    def pack_widgets(self):
        for key, widget in self.w.items():
            self.add(widget, text=key)
            # widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def save_button(self):
        pass

    def load_button(self):
        pass