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
        self.json_rw = master.json_rw
        self.refresh_bind_func = None
        self.get_memo_dict = None
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
        self.get_memo_dict()
        self.json_rw.write(self.SP.server_dir, SP=self.SP, GP=self.GP, MEMO=self.MEMO)
        self.logger.debug("write json data")
        self.load_button()

    def load_button(self):
        SD = DS.read_schedule_data(self.SP.server_dir)
        for key, df in SD.items():
            self.SD[key] = df
        self.logger.debug("read schedule data")
        SP, GP, MEMO = self.json_rw.read()
        self.parameter_update(SP, GP, MEMO)
        self.logger.debug("read json data")
        self.refresh_bind_func()

    def date_update_callback(self, date):
        self.OB["Date"] = date
        self.logger.debug(f"update OB['date'] to {self.OB['Date']}")
        self.refresh_bind_func()

    def user_change_callback(self, member):
        self.OB["Member"] = member
        self.logger.debug(f"update OB['Member'] to {self.OB['Member']}")
        self.refresh_bind_func()

    def parameter_update(self, SP, GP, MEMO):
        for var in vars(SP):
            setattr(self.SP, var, getattr(SP, var))
        for var in vars(GP):
            setattr(self.GP, var, getattr(GP, var))
        self.MEMO["Memo"] = MEMO["Memo"]
        