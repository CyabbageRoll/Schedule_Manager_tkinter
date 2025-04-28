# default
from collections import OrderedDict
import tkinter as tk
import datetime
# user
import D_SubFrames as sf


class RecentSettingButtons(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.GP = master.GP
        self.update_recent_area_bind = None
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()
        self.update_prj_combo_func = None
        self.update_date_combo_func = None

    def set_variables(self):
        self.buttons1 = [["Display", self.update_recent_area],]
        self.buttons2 = [["1day", lambda x=-0:self.set_from_day(x)],
                         ["3days", lambda x=-2:self.set_from_day(x)],
                         ["5days", lambda x=-4:self.set_from_day(x)],
                         ["Week", lambda x=-6:self.set_from_day(x)],
                         ["Month", lambda x=-30:self.set_from_day(x)]]

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["From_date"] = sf.DateInputBox(self)
        self.w["Label"] = tk.Label(self, text="~", font=self.font)
        self.w["End_date"] = sf.DateInputBox(self)
        self.w["Display"] = sf.ButtonRow(self, self.buttons1)
        self.w["Buttons"] = sf.ButtonRow(self, self.buttons2)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = False
            widget.pack(side=tk.LEFT, fill=f, expand=e)

    def set_init(self):
        self.set_from_day(-7)

    def set_from_day(self, days):
        if isinstance(days, int):
            self.w["From_date"].set(datetime.date.today() + datetime.timedelta(days=days))
        self.update_recent_area()

    def update_recent_area(self):
        if self.update_recent_area_bind is not None:
            self.update_recent_area_bind()

    def set_bind(self):
        # up-down-boxのbindはそれぞれのクラスの中に定義されている
        # self.w["prj_type"].w["Box"].bind("<<ComboboxSelected>>", self.update_prj_combo)
        # self.w["date_type"].w["Box"].bind("<<ComboboxSelected>>", self.update_date_combo)
        pass

    def get_date(self):
        return (self.w["From_date"].get(), self.w["End_date"].get())