# default
from collections import OrderedDict
import tkinter as tk
# user
import D_SubFrames as sf


class SettingButtons(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.GP = master.GP
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()
        self.update_prj_combo_func = None
        self.update_date_combo_func = None

    def set_variables(self):
        self.class_list = ["Project1", "Project2", "Project3", "Project4", "Task"]
        self.class_dict = {k: i + 2 for i, k in enumerate(self.class_list)}
        self.calender_list = ["Daily", "Weekly", "Monthly"]

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["prj_type"] = sf.LabelCombo(self, label_txt="Display Type",
                                           label_width=15,
                                           init_value=self.class_list[self.SP.schedule_prj_type-2],
                                           state="readonly",
                                           combo_list=self.class_list)
        self.w["date_type"] = sf.LabelCombo(self, label_txt="Calender Type",
                                            label_width=15,
                                            init_value=self.SP.schedule_calender_type,
                                            state="readonly",
                                            combo_list=self.calender_list)
        self.w["font"] = sf.UpDownBox(self, label="font_size", min_value=1, max_value=100, init_value=self.GP.schedule_font_size)
        self.w["width"] = sf.UpDownBox(self, label="task_width", min_value=1, max_value=100, init_value=self.SP.schedule_width)
        self.w["day_hour"] = sf.UpDownBox(self, label="h/day", min_value=1, max_value=10, init_value=self.SP.daily_task_hour)
        self.w["color_label"] = tk.Label(self, text="BackColor", font=self.font)
        self.w["color"] = sf.ColorSelector(self, init_color=self.GP.schedule_bg_color)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = False
            widget.pack(side=tk.LEFT, fill=f, expand=e)

    def set_init(self):
        pass

    def set_bind(self):
        # up-down-boxのbindはそれぞれのクラスの中に定義されている
        self.w["prj_type"].w["Box"].bind("<<ComboboxSelected>>", self.update_prj_combo)
        self.w["date_type"].w["Box"].bind("<<ComboboxSelected>>", self.update_date_combo)

    def update_prj_combo(self, event):
        self.update_prj_combo_func()

    def update_date_combo(self, event):
        self.update_date_combo_func()

    def get_font_size(self):
        return self.w["font"].get()

    def get_width(self):
        return self.w["width"].get()
    
    def get_day_hour(self):
        return self.w["day_hour"].get()
    
    def get_calender_type(self):
        return self.w["date_type"].get()
    
    def get_prj_type(self):
        return self.class_dict[self.w["prj_type"].get()]
    
    def get_bg_color(self):
        return self.w["color"].get_as_hex()