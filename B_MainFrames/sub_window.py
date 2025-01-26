import tkinter as tk
from tkinter import ttk
from collections import OrderedDict
# user
import A_DataSettingRW as ds
import C_Tab01_DailyTable as tab1
import C_Tab02_Project as tab2
import C_Tab03_ProjectManage as tab3
import C_Tab04_ScheduleTask as tab4


class SubWindow(ttk.Notebook):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SP = master.SP
        self.SD = master.SD
        self.OB = master.OB

        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.logger.debug("initialized Command Window")

    def set_variables(self):
        pass

    def set_init(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        # self.w["Schedule-Task"] = mf.ScheduleTask(self, bg="#ee5555")
        self.w["Projects-Display"] = tab2.ProjectDisplay(self, bg="#ee2222")
        self.w["Project-Manage"] = tab3.ProjectManage(self, bg="#3333ee")
        self.w["Daily"] = tab1.DailyInformation(self, bg="#5555ee")
        self.w["Memo"] = tk.Frame(self, bg="#7777ee")

    def pack_widgets(self):
        for key, widget in self.w.items():
            self.add(widget, text=key)
            # widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def save_button(self):
        ds.save_df_as_pkl(self.SD, self.SP.server_dir)

    def load_button(self):
        self.SD = ds.read_schedule_data(self.SP.server_dir)