# default
from collections import OrderedDict
import tkinter as tk
# user
import D_SubFrames as sf


class SettingButtons(tk.Frame):
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
        self.w["font"] = sf.UpDownBox(self, label="font_size", min_value=1, max_value=100, init_value=10)
        self.w["width"] = sf.UpDownBox(self, label="task_width", min_value=1, max_value=100, init_value=10)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = False
            widget.pack(side=tk.LEFT, fill=f, expand=e)

    def set_init(self):
        pass

    def set_bind(self):
        pass

    def get_font_size(self):
        return self.w["font"].get()

    def get_width(self):
        return self.w["width"].get()