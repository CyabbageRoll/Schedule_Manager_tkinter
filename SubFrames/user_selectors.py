from collections import OrderedDict
import tkinter as tk
from tkinter import ttk


class UserSelectors(tk.Frame):
    def __init__(self, master, callback_dict={}, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SP = master.SP
        self.GP = master.GP
        self.SD = master.SD
        self.MEMO = master.MEMO

        self.call_back_select_user = callback_dict.get("select_user", lambda : None)
        # self.call_back_code1_selector = callback_dict.get("code1_selector", lambda : None)
        # self.call_back_code2_selector = callback_dict.get("code2_selector", lambda : None)
        # self.call_back_code3_selector = callback_dict.get("code3_selector", lambda : None)
        # self.call_back_code4_selector = callback_dict.get("code4_selector", lambda : None)
        # self.call_back_prj_selector = callback_dict.get("prj_selector", lambda : None)

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
        # self.w["code1_selector"] = tk.Button(self, text="Code1", width=s, height=s, command=self.code1_selector)
        # self.w["code2_selector"] = tk.Button(self, text="Code2", width=s, height=s, command=self.code2_selector)
        # self.w["code3_selector"] = tk.Button(self, text="Code3", width=s, height=s, command=self.code3_selector)
        # self.w["code4_selector"] = tk.Button(self, text="Code4", width=s, height=s, command=self.code4_selector)
        # self.w["Project_selector"] = tk.Button(self, text="Project", width=s, height=s, command=self.prj_selector)

    def pack_widgets(self):
        for key, widget in self.w.items():
            self.logger.debug(key)
            widget.pack(side=tk.LEFT ,fill=tk.BOTH, expand=True)

    def set_bind(self):
        self.w["user_selector"].bind("<<ComboboxSelected>>", self.select_user)

    def select_user(self, event):
        self.call_back_select_user(self.display_user.get())

    # def code1_selector(self):
    #     self.call_back_code1_selector()

    # def code2_selector(self):
    #     self.call_back_code2_selector()

    # def code3_selector(self):
    #     self.call_back_code3_selector()

    # def code4_selector(self):
    #     self.call_back_code4_selector()

    # def prj_selector(self):
    #     self.call_back_prj_selector()








