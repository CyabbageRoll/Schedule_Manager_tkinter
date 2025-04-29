import tkinter as tk
from tkinter import ttk
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
        self.INFO = master.INFO
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
        self.w["save_button"] = ttk.Button(self, text="Save", width=s, command=self.save_button, style="My.TButton")
        self.w["load_button"] = ttk.Button(self, text="Load", width=s, command=self.load_button, style="My.TButton")

    def pack_widgets(self):
        for key, widget in self.w.items():
            widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def save_button(self):
        DS.save_schedule_data(self.logger, self.SD, self.SP.server_dir, self.SP.user)
        self.logger.debug("save schedule data")
        self.get_memo_dict()
        self.json_rw.write(self.SP.server_dir, SP=self.SP, GP=self.GP, MEMO=self.MEMO, BUG_REP=self.INFO["Report"])
        self.logger.debug("write json data")
        self.load_button(with_message=False)
        self._show_timed_popup("保存しました")

    def load_button(self, with_message=True):
        SD = DS.read_schedule_data(self.logger, self.SP.server_dir)
        for key, df in SD.items():
            self.SD[key] = df
        self.logger.debug("read schedule data")
        SP, GP, MEMO, INFO = self.json_rw.read()
        self.parameter_update(SP, GP, MEMO, INFO)
        self.logger.debug("read json data")
        self.refresh_bind_func()
        if with_message:
            self._show_timed_popup("ロードしました")

    def date_update_callback(self, date):
        self.OB["Date"] = date
        self.logger.debug(f"update OB['date'] to {self.OB['Date']}")
        self.refresh_bind_func()

    def user_change_callback(self, member):
        self.OB["Member"] = member
        self.logger.debug(f"update OB['Member'] to {self.OB['Member']}")
        self.refresh_bind_func()

    def parameter_update(self, SP, GP, MEMO, INFO):
        for var in vars(SP):
            setattr(self.SP, var, getattr(SP, var))
        for var in vars(GP):
            setattr(self.GP, var, getattr(GP, var))
        self.MEMO["Memo"] = MEMO["Memo"]
        self.INFO["Versions"] = INFO.get("Versions", "")
        self.INFO["Report"] = INFO.get("Report", "")
    
    def _show_timed_popup(self, message, duration=1000):
        root = tk.Tk()
        root.withdraw()
        popup = tk.Toplevel(root)
        popup.title("Information")
        label = tk.Label(popup, text=message)
        label.pack(padx=20, pady=20)
        root.after(duration, popup.destroy)
        root.after(duration, root.destroy)
        popup.mainloop()