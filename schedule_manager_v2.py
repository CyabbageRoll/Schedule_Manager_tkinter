# libraries
# default
import os
import tkinter as tk
import tkinter.font
from tkinter import ttk

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

        self.tk_setting()
        self.set_frames()
        self.grid_frames()

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
        self.rw = mf.SubWindow(self, height=500, width=350)
        self.dw = mf.MainWindow(self, height=500, width=550)

    def grid_frames(self):
        self.ob.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        self.rw.grid(row=1, column=0, sticky=tk.NSEW)
        self.dw.grid(row=1, column=1, sticky=tk.NSEW)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)


if __name__ == "__main__":
    sch_app = ScheduleManager()
    sch_app.mainloop()