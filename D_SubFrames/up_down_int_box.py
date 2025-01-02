# default
from collections import OrderedDict
import tkinter as tk
# additional
import pandas as pd
# user
import D_SubFrames as sf


class UpDownBox(tk.Frame):
    def __init__(self, master, label=None, min_value=0, max_value=99, init_value=10, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.min = min_value
        self.max = max_value
        self.current_value = init_value
        self.label = label
        self.add_bind_func = None
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init(init_value)
        self.set_bind()

    def set_variables(self):
        self.value = tk.StringVar()

    def set_widgets(self):
        self.w = OrderedDict()
        if self.label:
            self.w["label"] = tk.Label(self, text=self.label, font=self.font)
        self.w["M"] = tk.Button(self, text="-", command=self.click_m, font=self.font)
        self.w["Box"] = tk.Entry(self, 
                                 textvariable=self.value,
                                 justify=tk.CENTER,
                                 width=10,
                                 font=self.font)
        self.w["P"] = tk.Button(self, text="+", command=self.click_p, font=self.font)

    def pack_widgets(self):
        for k, widget in self.w.items():
            widget.pack(side=tk.LEFT, fill=tk.X, expand=False)

    def set_init(self, init_value):
        self.set(init_value)

    def set_bind(self):
        self.w["Box"].bind("<Return>", self.box_focus_out)
        self.w["Box"].bind("<FocusOut>", self.box_focus_out)

    def box_focus_out(self, event):
        if self.is_able_to_change_int(self.get()):
            self.apply_max_min()
        else:
            self.set(self.current_value)

    def is_able_to_change_int(self, v):
        try:
            v = int(v)
            return True
        except:
            return False

    def get(self):
        return self.value.get()

    def set(self, value):
        self.value.set(value)
        self.current_value = value
        if self.add_bind_func is not None:
            self.add_bind_func()

    def click_m(self):
        self.update_value(-1)

    def click_p(self):
        self.update_value(+1)

    def update_value(self, pm):
        v = int(self.get())
        v += pm
        self.set(v)

    def apply_max_min(self):
        v = int(self.get())
        v = min(max(v, self.min), self.max)
        self.set(v)