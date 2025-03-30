# default
from collections import OrderedDict
import tkinter as tk
from tkinter import ttk
# user
import D_SubFrames as sf


class UserCommandButtons(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.OB = master.OB
        self.MEMO = master.MEMO
        self.Buttons = ["Command01", "Command02", "Command03", "Command04", "Command05"]
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()


    def set_variables(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        for i, button in enumerate(self.Buttons):
            self.w[f"B{i+1:02d}"] = ttk.Button(self, text=button, command=lambda k=i+1:self.press_command(f"B{k:02d}"), style="TButton")

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def refresh(self):
        pass

    def set_init(self):
        self.refresh()

    def set_bind(self):
        pass

    def press_command(self, button_idx):
        self.logger.debug(f"press user command button {button_idx}")
        print(f"press user command button {button_idx}")

