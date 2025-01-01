from collections import OrderedDict
import tkinter as tk
from tkinter import ttk


class ButtonRow(tk.Frame):
    def __init__(self, master, buttons, **kwargs):
        """buttons = [[text, callback]]"""
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        # self.set_variables()
        self.set_widgets(buttons)
        self.pack_widgets()
        # self.set_init()

    def set_variables(self):
        pass

    def set_widgets(self, buttons):
        self.w = OrderedDict()
        for txt, cb in buttons:
            self.w[txt] = tk.Button(self, text=txt, command=cb, font=self.font)
    
    def pack_widgets(self):
        for key, widget in self.w.items():
            widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def set_init(self, label_txt, init_txt):
        pass
