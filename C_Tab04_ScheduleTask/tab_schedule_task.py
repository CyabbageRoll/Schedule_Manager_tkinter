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
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["inp_box"] = tab4.SettingButtons(self)
        self.w["schedule"] = tab4.ScrollableScheduleArea(self)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = False if k == "inp_box" else True
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def set_init(self):
        self.set_bind()

    def set_bind(self):
        self.w["inp_box"].w["font"].add_bind_func = self.update_func
        self.w["inp_box"].w["width"].add_bind_func = self.update_func

    def update_func(self, v):
        font_size = self.w["inp_box"].get_font_size()
        schedule_width = self.w["inp_box"].get_width()
        self.SP.font_size = font_size
        self.SP.schedule_width = schedule_width
        self.w["schedule"].update(v)