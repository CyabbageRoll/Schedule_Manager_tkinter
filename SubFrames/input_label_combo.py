from collections import OrderedDict
import tkinter as tk
from tkinter import ttk

class LabelCombo(tk.Frame):
    def __init__(self, master, 
                 label_txt="label", init_txt="", label_width_ratio=2, state="normal", combo_list=[],
                 **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.set_variables(combo_list)
        self.set_widgets(label_width_ratio, state)
        self.pack_widgets()
        self.set_init(label_txt, init_txt)
        # self.logger.debug("label combo DataSelectorButton")

    def set_variables(self, combo_list):
        self.display_text = tk.StringVar()
        self.combo_list = combo_list
        self.label = tk.StringVar()

    def set_widgets(self, label_width, state):
        self.w = OrderedDict()
        self.w["Label"] = tk.Label(self, textvariable=self.label, width=label_width, font=self.font)
        self.w["Combobox"] = ttk.Combobox(self,
                                          textvariable=self.display_text,
                                          values=self.combo_list,
                                          width=10,
                                          height=10,
                                          font=self.font,
                                          state=state)
    
    def pack_widgets(self):
        for key, widget in self.w.items():
            f = tk.Y if key == "Label" else tk.BOTH
            e = False if key == "Label" else True
            widget.pack(side=tk.LEFT, fill=f, expand=e)

    def set_init(self, label_txt, init_txt):
        self.display_text.set(init_txt)
        self.label.set(label_txt)

    def set(self, str):
        self.display_text.set(str)

    def get(self):
        return self.display_text.get()


class InputListArea(tk.Frame):
    def __init__(self, master, label_combo_dict, **kwargs):
        """label_combo : {label_text: [initial value, [combobox item list], state, label_width_ratio]} """
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font

        self.set_variables()
        self.set_widgets(label_combo_dict)
        self.pack_widgets()
        self.set_init()

    def set_variables(self):
        pass

    def set_widgets(self, label_combo_dict):
        self.w = OrderedDict()
        for k, v in label_combo_dict.items():
            self.w[k] = LabelCombo(self, 
                                   label_txt=k,                 
                                   init_txt=v[0],
                                   combo_list=v[1],
                                   state=v[2],
                                   label_width_ratio=v[3])

    def pack_widgets(self):
        for key, widget in self.w.items():
            widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def set_init(self):
        pass

    def set(self, k, str):
        self.w[k].set(str)

    def get(self, k):
        return self.w[k].get()
    
    def set_list(self, k, l):
        self.w[k].w["Combobox"]["values"] = l

    def get_list(self, k):
        return self.w[k].w["Combobox"]["values"]