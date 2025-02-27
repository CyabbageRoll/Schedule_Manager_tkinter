import tkinter as tk
from collections import OrderedDict

import A_DataSettingRW as DS
import D_SubFrames as sf

class OptionBar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SP = master.SP
        self.GP = master.GP
        self.SD = master.SD
        self.OB = master.OB
        self.MEMO = master.MEMO
        self.refresh_bind_func = None
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
        self.w["date_selector"] = sf.DateSelectorButton(self, date_update_callback=self.date_update_callback)
        self.w["selector"] = sf.UserSelector(self, user_change_callback=self.user_change_callback)
        self.w["save_button"] = tk.Button(self, text="Save", width=s, height=s, command=self.save_button, font=self.font)
        self.w["load_button"] = tk.Button(self, text="Load", width=s, height=s, command=self.load_button, font=self.font)

    def pack_widgets(self):
        for key, widget in self.w.items():
            widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def save_button(self):
        DS.save_schedule_data(self.SD, self.SP.server_dir)
        self.logger.debug("save schedule data")

    def load_button(self):
        self.SD = DS.read_schedule_data(self.SP.server_dir)
        self.logger.debug("read schedule data")

    def date_update_callback(self, date):
        self.OB["Date"] = date
        self.logger.debug(f"update OB['date'] to {self.OB['Date']}")
        self.refresh_bind_func()

    def user_change_callback(self, member):
        self.OB["Member"] = member
        self.logger.debug(f"update OB['Member'] to {self.OB['Member']}")
        self.refresh_bind_func()
