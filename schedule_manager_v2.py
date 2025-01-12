# libraries
# default
import os
import tkinter as tk
import tkinter.font
from tkinter import ttk
import datetime

# user
import A_DataSettingRW as DS
import B_MainFrames as mf
import utils as ut


class ScheduleManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logger = ut.logger_settings()
        p_dir = os.path.dirname(os.path.dirname(__file__))
        json_rw = DS.JSONReadWrite(p_dir, self.logger)
        self.SP, self.GP, self.MEMO = json_rw.read()
        self.SD = DS.read_schedule_data(self.SP.server_dir)
        self.OB = {"Member": self.SP.user, "Date": datetime.date.today().strftime(r"%Y-%m-%d")}

        self.tk_setting()
        self.set_frames()
        self.grid_frames()
        self.set_binds()
        self.init()

    def tk_setting(self):
        self.font = tkinter.font.Font(self, family=self.GP.font_family, size=self.GP.font_size)
        self.title("Schedule App")
        self.geometry(f"{self.GP.window_width}x{self.GP.window_height}")
        self.configure(bg=self.GP.window_bg_color)

        s = ttk.Style()
        s.configure('TNotebook.Tab', font=self.font)
        s.configure('Treeview', font=self.font)
        s.configure('Treeview.Heading', font=self.font)

    def set_frames(self):
        self.ob = mf.OptionBar(self, bg="#e09999", height=100, width=900)
        self.sw = mf.SubWindow(self, height=500, width=350)
        self.mw = mf.MainWindow(self, height=500, width=550)

    def grid_frames(self):
        self.ob.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        self.sw.grid(row=1, column=0, sticky=tk.NSEW)
        self.mw.grid(row=1, column=1, sticky=tk.NSEW)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def set_binds(self):
        self.sw.w["Project-Manage"].add_bind_func = self.refresh
        self.mw.w["Schedule-Task"].w["schedule"].click_bind_func = self.task_click
    
    def task_click(self, class_idx, idx):
        current_tab = self.sw.select()
        if class_idx == 6:
            if current_tab == ".!subwindow.!dailyinformation":
                ds = self.SD[class_idx].loc[idx, :]
                self.sw.w["Daily"].update_item(ds)

    def refresh(self):
        print("refresh")
        self.logger.debug("refresh")
        self.mw.w["Schedule-Task"].update()

    def init(self):
        # self.task_click(6, "250103_cb12")
        # for key in self.SD:
        #     print(key)
        #     print(self.SD[key])
        pass


if __name__ == "__main__":
    sch_app = ScheduleManager()
    sch_app.mainloop()