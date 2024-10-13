# default
from collections import OrderedDict
import tkinter as tk
# additional
import pandas as pd
# user
import SubFrames as sf


class ProjectManage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.prj_item = {i+1: "" for i in range(4)}
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["Selector"] = sf.ProjectSelector(self)
        self.w["Input"] = sf.ProjectManageInput(self)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = True
            widget.pack(side=tk.LEFT, fill=f, expand=e)

    def set_init(self):
        self.w["Selector"].changed = self.w["Input"].set

    def set_bind(self):
        pass