import tkinter as tk
from tkinter import ttk
from collections import OrderedDict
# user
import SubFrames as sf
import MainFrames as mf
import DataSettingRW as ds


class SubWindow(ttk.Notebook):
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
        self.w["Daily"] = mf.DailyInformation(self, bg="#5555ee")
        self.w["Task"] = mf.TaskCreator(self, bg="#4444ee")
        self.w["Ticket"] = tk.Frame(self, bg="#2222ee")
        self.w["Team"] = tk.Frame(self, bg="#6666ee")
        self.w["Memo"] = tk.Frame(self, bg="#7777ee")

    def pack_widgets(self):
        for key, widget in self.w.items():
            self.add(widget, text=key)
            # widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def save_button(self):
        ds.save_df_as_pkl(self.SD, self.SP.server_dir)

    def load_button(self):
        self.SD = ds.read_schedule_data(self.SP.server_dir)