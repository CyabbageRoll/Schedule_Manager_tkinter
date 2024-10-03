import tkinter as tk
from collections import OrderedDict

import SubFrames as sf


class OptionBar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SP = master.SP
        self.GP = master.GP
        self.SD = master.SD
        self.MEMO = master.MEMO
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.logger.debug("initialized OptionBar")

    def set_variables(self):
        pass

    def set_init(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        s = 1
        self.w["date_selector"] = sf.DateSelectorButton(self)
        self.w["selector"] = sf.UserSelectors(self)
        self.w["save_button"] = tk.Button(self, text="Save", width=s, height=s, command=self.save_button, font=self.font)
        self.w["load_button"] = tk.Button(self, text="Load", width=s, height=s, command=self.load_button, font=self.font)


    def pack_widgets(self):
        for key, widget in self.w.items():
            widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def save_button(self):
        pass

    def load_button(self):
        pass