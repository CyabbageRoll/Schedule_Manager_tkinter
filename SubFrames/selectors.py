from collections import defaultdict
import tkinter as tk
from tkinter import ttk


class Selectors(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.SP = master.SP
        self.SD = master.SD

        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()
        self.logger.debug("initialized Selectors")

    def set_variables(self):
        self.user = tk.StringVar()
        self.members = [self.SP.user] + self.SP.members

    def set_init(self):
        self.user.set(self.SP.user)

    def set_widgets(self):
        self.w = defaultdict(list)
        s = 1
        self.w["user_selector"] = ttk.Combobox(self, 
                                               textvariable=self.user,
                                               values=self.members,
                                               height=10, width=15, 
                                               state="readonly")
        self.w["code1_selector"] = tk.Button(self, text="Code1", width=s, height=s, command=self.code1_selector)
        self.w["code2_selector"] = tk.Button(self, text="Code2", width=s, height=s, command=self.code2_selector)
        self.w["code3_selector"] = tk.Button(self, text="Code3", width=s, height=s, command=self.code3_selector)
        self.w["code4_selector"] = tk.Button(self, text="Code4", width=s, height=s, command=self.code4_selector)
        self.w["Project_selector"] = tk.Button(self, text="Project", width=s, height=s, command=self.prj_selector)

    def pack_widgets(self):
        for key, widget in self.w.items():
            self.logger.debug(key)
            widget.pack(side=tk.LEFT ,fill=tk.BOTH, expand=True)

    def set_bind(self):
        self.w["user_selector"].bind("<<ComboboxSelected>>", self.select_user)

    def select_user(self, event):
        pass

    def code1_selector(self):
        pass

    def code2_selector(self):
        pass

    def code3_selector(self):
        pass

    def code4_selector(self):
        pass

    def prj_selector(self):
        pass

