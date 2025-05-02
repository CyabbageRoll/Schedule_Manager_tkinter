# default
from collections import OrderedDict
import tkinter as tk
import datetime
# additional
# user
import C_Tab04_ScheduleTask as tab4
import D_SubFrames as sf

class ScheduleTask(tk.Frame):
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
        self.display_type_list = ["Gantt", "Schedule"]

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["holidays"] = sf.LabelEntryBox(self, "Holidays", label_width=15, init_value=self.SP.schedule_holidays)
        self.w["inp_box2"] = tab4.SettingButtons2(self, self.display_type_list)
        self.w["inp_box"] = tab4.SettingButtons(self)
        self.w["label"] = tk.Label(self, textvariable=self.msg, font=self.font, anchor="w")
        self.w["schedule"] = tab4.ScrollableScheduleArea(self)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = True if k == "schedule" else False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def set_init(self):
        self.msg.set("information")

    def set_bind(self):
        self.w["inp_box"].update_prj_combo_func = lambda: self.update_func("prj")
        self.w["inp_box"].update_date_combo_func = lambda: self.update_func("calendar")
        self.w["inp_box"].w["font"].add_bind_func = lambda: self.update_func("font")
        self.w["inp_box"].w["width"].add_bind_func = lambda: self.update_func("width")
        self.w["inp_box"].w["day_hour"].add_bind_func = lambda: self.update_func("day_hour")
        self.w["inp_box"].w["color"].add_bind_func = lambda: self.update_func("color")
        self.w["schedule"].w["area"].label_update_func = self.set_label
        self.w["holidays"].bind_func_return_callback = lambda: self.update_func("calendar")
        self.w["holidays"].bind_func_focus_out_callback = lambda: self.update_func("calendar")
        self.w["inp_box2"].call_back_func_radio = self.display_type_radio_update
        self.w["inp_box2"].call_back_func_date = self.display_type_date_update

    def update_func(self, mode=None):
        self.GP.schedule_font_size = int(self.w["inp_box"].get_font_size())
        self.SP.schedule_width = int(self.w["inp_box"].get_width())
        self.SP.daily_task_hour = int(self.w["inp_box"].get_day_hour())
        self.GP.schedule_bg_color = str(self.w["inp_box"].get_bg_color())
        if mode == "calendar":
            self.store_valid_holidays()
        if mode == "prj":
            prj_type = self.w["inp_box"].get_prj_type()
            self.SP.schedule_prj_type = prj_type
            self.w["schedule"].w["area"].class_idx = prj_type
            # prj typeが1~4の時は、scheduleの月表示、5はGantt表示で週、6はGanntt表示で日にする
            if prj_type in [1, 2, 3, 4]:
                self.w["inp_box2"].w["display_type"].set("Schedule")
                self.SP.schedule_display_type = "Schedule"
                self.w["inp_box"].w["date_type"].set("Monthly")
            if prj_type in [5, 6]:
                self.w["inp_box2"].w["display_type"].set("Gantt")
                self.SP.schedule_display_type = "Gantt"
                if prj_type == 5:
                    self.w["inp_box"].w["date_type"].set("Weekly")
                if prj_type == 6:
                    self.w["inp_box"].w["date_type"].set("Daily")

        calendar_type = self.w["inp_box"].get_calendar_type()
        self.SP.schedule_calendar_type = calendar_type
        self.w["schedule"].w["area"].calendar_type = calendar_type
        self.w["schedule"].update(mode="both")

    def update(self, mode="both"):
        self.w["schedule"].update(mode)

    def set_label(self, txt):
        self.msg.set(txt)

    def store_valid_holidays(self):
        holidays = self.w["holidays"].get()
        try:
            holidays = holidays.replace(",", " ")
            holidays = [x.strip().upper() for x in holidays.split(" ") if x]
            holidays = list(set(holidays))
            date_box = sf.DateInputBox(self)
            holiday_weekdays, holiday_datetime = [], []
            for s in holidays:
                if s in ["SUN", "SAT", "MON", "TUE", "WED", "THU", "FRI"]:
                    holiday_weekdays.append(s)
                else:
                    holiday_datetime.append(date_box.str2date(s))
            self.SP.schedule_holidays = holiday_weekdays + [d.strftime("%Y/%m/%d") for d in holiday_datetime]
            self.w["holidays"].set(self.SP.schedule_holidays)
        except Exception as e:
            self.logger.error(f"Error: {e}")
            holidays = []

    def display_type_radio_update(self, ret):
        self.SP.schedule_display_type = ret
        self.update_func(mode="both")

    def display_type_date_update(self, ret):
        str_date = self.w["inp_box2"].w["start_date"].get_str_date()
        self.SP.schedule_start_date = str_date.replace("/", "-")
        self.update_func(mode="both")