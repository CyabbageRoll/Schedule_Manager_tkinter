# libraries
# default
import os
import tkinter as tk

# additional


# user
import DataSettingRW as ds
import MainFrames as mf
# import SubFrames as sf
import utils


class ScheduleManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logger = utils.logger_settings()
        self.SP = ds.SettingParameters()
        self.GP = ds.GUIParameters()
        self.SD = ds.ScheduleData()
        self.tk_setting()
        self.set_frames()
        self.grid_frames()

    def tk_setting(self):
        self.title("Schedule App")
        self.geometry(f"{self.GP.window_width}x{self.GP.window_height}")
        self.configure(bg=self.GP.window_bg_color)

    def set_frames(self):
        self.ob = mf.OptionBar(self, bg="#e09999", height=100, width=900)
        self.rw = mf.CommandWindow(self, height=500, width=300)
        self.dw = mf.DisplayWindow(self, height=500, width=600)

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