# default
from collections import OrderedDict
import tkinter as tk
# additional
# user
import C_Tab04_ScheduleTask as tab4

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

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["label"] = tk.Label(self, textvariable=self.msg, font=self.font, anchor="w")
        self.w["inp_box"] = tab4.SettingButtons(self)
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
        self.w["inp_box"].update_date_combo_func = lambda: self.update_func("calender")
        self.w["inp_box"].w["font"].add_bind_func = lambda: self.update_func("font")
        self.w["inp_box"].w["width"].add_bind_func = lambda: self.update_func("width")
        self.w["inp_box"].w["color"].add_bind_func = lambda: self.update_func("color")
        self.w["schedule"].w["area"].label_update_func = self.set_label

    def update_func(self, mode=None):
        self.GP.schedule_font_size = int(self.w["inp_box"].get_font_size())
        self.SP.schedule_width = int(self.w["inp_box"].get_width())
        self.GP.schedule_bg_color = str(self.w["inp_box"].get_bg_color())
        print(self.GP)
        if mode == "prj":
            prj_type = self.w["inp_box"].get_prj_type()
            self.SP.schedule_prj_type = prj_type
            self.w["schedule"].w["area"].class_idx = prj_type
        if mode == "calender":
            calender_type = self.w["inp_box"].get_calender_type()
            self.SP.schedule_calender_type = calender_type
            self.w["schedule"].w["area"].calender_type = calender_type
        self.w["schedule"].update(mode)

    def update(self, mode="both"):
        self.w["schedule"].update(mode)

    def set_label(self, txt):
        self.msg.set(txt)