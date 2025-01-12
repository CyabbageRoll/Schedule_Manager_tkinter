"""
Date Input Box
[    Date     ][weekday]
"""


from collections import OrderedDict
import datetime
import tkinter as tk
from dateutil.relativedelta import relativedelta


class DateInputBox(tk.Frame):
    def __init__(self, master, press_enter_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.press_enter_callback = press_enter_callback
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()
        self.logger.debug("initialized DateInputBox")

    def set_variables(self):
        self.v_date = tk.StringVar()
        self.v_weekday = tk.StringVar()

    def set_init(self):
        self.selected_date = datetime.date.today()
        self.update_display_date()

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["date_input_box"] = tk.Entry(self, textvariable=self.v_date, width=9, justify=tk.CENTER, font=self.font)
        self.w["weekday"] = tk.Label(self, textvariable=self.v_weekday, width=3, font=self.font)

    def pack_widgets(self):
        for key, widget in self.w.items():
            self.logger.debug(key)
            widget.pack(side=tk.LEFT ,fill=tk.BOTH, expand=True)

    def set_bind(self):
        self.w["date_input_box"].bind("<Return>", self.press_key)
        self.w["date_input_box"].bind("<FocusOut>", self.press_key)

    def update_display_date(self):
        self.v_date.set(self.date2str(self.selected_date))
        if isinstance(self.selected_date, datetime.date):
            www = self.selected_date.strftime(r"%a")
            self.v_weekday.set(www)

    def press_key(self, event):
        #入力内容を表示
        d = self.v_date.get()
        tmp = self.str2date(d)
        if tmp is None:
            return
        self.selected_date = tmp
        self.logger.debug(f"date update {d} -> {self.selected_date}")
        self.update_display_date()
        if self.press_enter_callback is not None:
            self.press_enter_callback(self.get())

    def date2str(self, date):
        if isinstance(date, str):
            str_date = date
        else:
            str_date = date.strftime(r"%Y/%m/%d")
        return str_date

    def str2date(self, str_date):
        str_date = str_date.replace(".", "/")
        str_date = str_date.replace(" ", "/")
        str_date = str_date.replace("／", "/")

        d_date = None
        if len(str_date) < 3:
            d_date = self.str2date_less3letters(str_date)
        elif len(str_date) < 6:
            d_date = self.str2date_less6letters(str_date)
        else:
            d_date = self.str2date_more6letters(str_date)
        return d_date

    def str2date_less3letters(self, dd):
        try:
            today = datetime.date.today()
            yyyymm = today.strftime(r"%Y/%m")
            str_date = yyyymm + "/" + dd
            d_date = datetime.datetime.strptime(str_date, r"%Y/%m/%d").date()
            if d_date < today:
                d_date += relativedelta(months=1)
            return d_date
        except Exception as E:
            self.logger.debug(E)
            return None
        
    def str2date_less6letters(self, mmdd):
        try:
            today = datetime.date.today()
            yyyy = today.strftime(r"%Y")
            str_date = yyyy + "/" + mmdd
            d_date = datetime.datetime.strptime(str_date, r"%Y/%m/%d").date()
            if d_date < today:
                d_date += relativedelta(years=1)
            return d_date
        except Exception as E:
            self.logger.debug(E)
            return None
        
    def str2date_more6letters(self, yymmdd):
        try:
            y = yymmdd.split("/")[0]
            if len(y) == 2:
                yymmdd = "20" + yymmdd
            d_date = datetime.datetime.strptime(yymmdd, r"%Y/%m/%d").date()
            return d_date
        except Exception as E:
            self.logger.debug(E)
            return None
        
    def set(self, date):
        self.selected_date = date
        if date is None:
            self.v_date.set("")
            self.v_weekday.set("")
        else:
            self.update_display_date()

    def get(self):
        return self.selected_date


if __name__ == "__main__":

    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils import logger_settings

    class TestTk(tk.Tk):
        def __init__(self):
            super().__init__()
            self.logger = logger_settings()

            self.geometry(f"400x400")
            self.frame = DateInputBox(self, press_enter_callback=self.enter_date_box)
            self.frame.pack(fill=tk.BOTH, expand=True)

        def enter_date_box(self):
            self.logger.debug("call back : press enter date box")
            return

    test_tk = TestTk()
    test_tk.mainloop()