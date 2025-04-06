from collections import OrderedDict
import tkinter as tk
from tkinter import ttk

import C_Tab01_DailyTable as tab1
import C_Tab02_Project as tab2
import C_Tab03_ProjectManage as tab3
import C_Tab04_ScheduleTask as tab4
import C_Tab05_ATT as tab5
import C_Tab06_TeamInfo as tab6
import C_Tab07_Regularly as tab7
import C_Tab08_Memo as tab8
import C_Tab09_Recent as tab9

class MainWindow(ttk.Notebook):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SP = master.SP
        self.SD = master.SD
        self.GP = master.GP
        self.OB = master.OB
        self.MEMO = master.MEMO

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
        self.w["Schedule"] = tab4.ScheduleTask(self)
        self.w["Regularly"] = tab7.Regularly(self)
        self.w["Team"] = tab6.TeamInfo(self)
        self.w["ATT"] = tab5.ATT(self)
        self.w["Projects-Display"] = tab2.ProjectDisplay(self)
        self.w["Recent"] = tab9.RecentTicket(self)
        self.w["Memo"] = tab8.TeamInfo(self)
        # self.w["Goals/Reflections"] = tk.Frame(self, bg="#555555")
        # self.w["Follows"] = tk.Frame(self, bg="#555555")

    def pack_widgets(self):
        for key, widget in self.w.items():
            self.add(widget, text=key)

    def save_button(self):
        pass

    def load_button(self):
        pass