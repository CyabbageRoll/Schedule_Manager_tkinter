import tkinter as tk

import DataSettingRW as ds
import MainFrames as mf
import SubFrames as sf
import utils


class TestTk(tk.Tk):
    def __init__(self, test_class):
        super().__init__()
        self.logger = utils.logger_settings()
        self.SP = ds.SettingParameters()
        self.GP = ds.GUIParameters()
        self.SD = ds.ScheduleData()

        self.geometry(f"400x400")
        self.frame = test_class()
        self.frame.pack()


test_tk = TestTk(test_class=mf.OptionBar)