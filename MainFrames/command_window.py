import tkinter as tk
from tkinter import ttk
from collections import OrderedDict

class CommandWindow(ttk.Notebook):
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
        self.w["Daily"] = tk.Frame(self, bg="#5555ee")
        self.w["Task1"] = tk.Frame(self, bg="#2222ee")
        self.w["Task2"] = tk.Frame(self, bg="#3333ee")
        self.w["Project"] = tk.Frame(self, bg="#4444ee")
        self.w["Team"] = tk.Frame(self, bg="#6666ee")
        self.w["Memo"] = tk.Frame(self, bg="#7777ee")

    def pack_widgets(self):
        for key, widget in self.w.items():
            self.add(widget, text=key)
            # widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def save_button(self):
        pass

    def load_button(self):
        pass