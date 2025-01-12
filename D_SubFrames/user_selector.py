from collections import OrderedDict
import tkinter as tk
from tkinter import ttk


class UserSelector(tk.Frame):
    def __init__(self, master, user_change_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SP = master.SP
        self.GP = master.GP
        self.SD = master.SD
        self.MEMO = master.MEMO

        self.user_change_callback = user_change_callback

        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()
        self.logger.debug("initialized Selectors")

    def set_variables(self):
        self.display_user = tk.StringVar()
        self.members = [self.SP.user] + self.SP.members

    def set_init(self):
        self.display_user.set(self.SP.user)

    def set_widgets(self):
        self.w = OrderedDict()
        # s = 1
        self.w["user_selector"] = ttk.Combobox(self, 
                                               textvariable=self.display_user,
                                               values=self.members,
                                               height=10, width=15, 
                                               state="readonly",
                                               font=self.font)

    def pack_widgets(self):
        for key, widget in self.w.items():
            self.logger.debug(key)
            widget.pack(side=tk.LEFT ,fill=tk.BOTH, expand=True)

    def set_bind(self):
        self.w["user_selector"].bind("<<ComboboxSelected>>", self.select_user)

    def select_user(self, event):
        if self.user_change_callback:
            self.user_change_callback(self.display_user.get())





