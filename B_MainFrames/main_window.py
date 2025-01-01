from collections import OrderedDict
import tkinter as tk
from tkinter import ttk

import C_Tab01_DailyTable as tab1
import C_Tab02_Project as tab2
import C_Tab03_ProjectManage as tab3
import C_Tab04_ScheduleTask as tab4


class MainWindow(ttk.Notebook):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SP = master.SP
        self.SD = master.SD

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
        # self.w["Project-Manage"] = mf.ProjectManage(self, bg="#3333ee")
        self.w["Schedule-Task"] = tab4.ScheduleTask(self, bg="#ee5555")
        self.w["Projects-Display"] = tab2.ProjectDisplay(self, bg="#ee2222")
        self.w["Schedule-Project"] = tk.Frame(self, bg="#ee5555")
        self.w["ATT-Task"] = tk.Frame(self, bg="#ee5555")
        self.w["ATT-Project"] = tk.Frame(self, bg="#ee4444")
        self.w["Regularly"] = tk.Frame(self, bg="#ee2222")
        self.w["Follows"] = tk.Frame(self, bg="#ee5555")

    def pack_widgets(self):
        for key, widget in self.w.items():
            self.add(widget, text=key)
            # widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def save_button(self):
        pass

    def load_button(self):
        pass