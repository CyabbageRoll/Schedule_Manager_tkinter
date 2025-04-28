from collections import OrderedDict
import tkinter as tk
from tkinter import ttk


class RadioButtons(tk.Frame):
    def __init__(self, master, buttons, init_idx=0, init_txt=None, call_back=None, vertical=False, **kwargs):
        """buttons = [[text, callback]]"""
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.call_back_func = call_back
        init_txt = init_txt if init_txt else buttons[init_idx]
        self.set_variables(init_txt)
        self.set_widgets(buttons)
        self.pack_widgets(vertical)
        # self.set_init()

    def set_variables(self, init_txt):
        self.var = tk.StringVar(value=init_txt)

    def set_widgets(self, buttons):
        self.w = OrderedDict()
        for txt in buttons:
            self.w[txt] = ttk.Radiobutton(self, text=txt, value=txt, variable=self.var, command=lambda x=txt: self._call_back_func(x))
        # style="My.TButton"
    
    def pack_widgets(self, vertical):
        side = tk.TOP if vertical else tk.LEFT
        for key, widget in self.w.items():
            widget.pack(side=side, fill=tk.BOTH, expand=True)

    def _call_back_func(self, x):
        if self.call_back_func is not None:
            self.call_back_func(x)