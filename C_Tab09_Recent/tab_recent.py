# default
from collections import OrderedDict
import tkinter as tk
# additional
# user
import C_Tab09_Recent as tab9

class RecentTicket(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.GP = master.GP
        self.OB = master.OB
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        self.msg = tk.StringVar()

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["label"] = tk.Label(self, textvariable=self.msg, font=self.font, anchor="w")
        self.w["inp_box"] = tab9.RecentSettingButtons(self)
        self.w["recent"] = tab9.ScrollableRecentArea(self)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = True if k == "schedule" else False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def set_init(self):
        self.msg.set("information")

    def set_bind(self):
        self.w["inp_box"].update_recent_area_bind = self.update
        self.w["recent"].w["area"].label_update_func = self.set_label

    def update_func(self, mode=None):
        self.update(mode)

    def update(self, mode=None):
        print("update func")
        display_date = self.w["inp_box"].get_date()
        self.w["recent"].update(display_date, mode)

    def set_label(self, txt):
        self.msg.set(txt)