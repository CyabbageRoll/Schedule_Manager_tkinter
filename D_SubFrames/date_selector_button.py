from collections import OrderedDict
import datetime
import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import D_SubFrames as sf


class DateSelectorButton(tk.Frame):
    def __init__(self, master, date_update_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.date_update_callback = date_update_callback
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.logger.debug("initialized DataSelectorButton")

    def set_variables(self):
        self.v_date = tk.StringVar()

    def set_init(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        s = 1
        self.w["left_arrow"] = ttk.Button(self, text="◀️", width=s, command=self.click_left, style="My.TButton")
        self.w["date_box"] = sf.DateInputBox(self, press_enter_callback=self.date_update_callback, height=s)
        self.w["right_arrow"] = ttk.Button(self, text="▶️", width=s, command=self.click_right, style="My.TButton")
        self.w["move_today"] = ttk.Button(self, text="Today", width=s, command=self.click_today, style="My.TButton")

    def pack_widgets(self):
        for key, widget in self.w.items():
            widget.pack(side=tk.LEFT ,fill=tk.BOTH, expand=True)

    def click_left(self):
        self.move_date(-1)

    def click_right(self):
        self.move_date(+1)

    def move_date(self, delta_day):
        dd = datetime.timedelta(days=delta_day)
        new_date = self.w["date_box"].selected_date + dd
        self.set_date(new_date)

    def click_today(self):
        self.set_date(datetime.date.today())

    def date2str(self, date):
        str_date = date.strftime(r"%Y/%m/%d")
        return str_date

    def date(self):
        return self.w["date_box"].selected_date
    
    def set_date(self, p_date):
        self.w["date_box"].selected_date = p_date
        self.w["date_box"].update_display_date()
        if self.date_update_callback:
            self.date_update_callback(p_date)

    # def str2date(str_date):
    #     date = datetime.datetime.strptime(str_date, "%Y/%m/%d")
    #     return date


if __name__ == "__main__":

    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils import logger_settings

    class TestTk(tk.Tk):
        def __init__(self, test_class):
            super().__init__()
            self.logger = logger_settings()

            self.geometry(f"400x400")
            self.frame = test_class(self)
            self.frame.pack(fill=tk.BOTH, expand=False)

    test_tk = TestTk(test_class=DateSelectorButton)
    test_tk.mainloop()