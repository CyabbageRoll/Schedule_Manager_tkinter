from collections import OrderedDict
import tkinter as tk
from tkinter import ttk

import SubFrames as sf


class LabelCombo(tk.Frame):
    def __init__(self, master, 
                 label_txt, init_txt="", label_width_ratio=2, state="normal", combo_list=[],
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
        self.set(init_txt)
        self.label.set(label_txt)

    def set(self, str):
        self.display_text.set(str)

    def get(self):
        return self.display_text.get()


class LabelDateInputBox(tk.Frame):
    def __init__(self, master,
                 label_txt="label", init_date="", label_width_ratio=2,
                 press_enter_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.set_variables()
        self.set_widgets(label_width_ratio, press_enter_callback)
        self.pack_widgets()
        self.set_init(label_txt, init_date)

    def set_variables(self):
        self.label = tk.StringVar()

    def set_widgets(self, label_width, press_enter_callback):
        self.w = OrderedDict()
        self.w["Label"] = tk.Label(self, textvariable=self.label, width=label_width, font=self.font)
        self.w["DateInputBox"] = sf.DateInputBox(self, 
                                                 press_enter_callback=press_enter_callback,
                                                 width=10, height=10)
        
    def pack_widgets(self):
        for key, widget in self.w.items():
            f = tk.Y if key == "Label" else tk.BOTH
            e = False if key == "Label" else True
            widget.pack(side=tk.LEFT, fill=f, expand=e)

    def set_init(self, label_txt, init_date):
        self.set(init_date)
        self.label.set(label_txt)

    def set(self, date):
        self.w["DateInputBox"].set(date)

    def get(self):
        return self.w["DateInputBox"].get()


class LabelColorSelector(tk.Frame):
    def __init__(self, master,
                label_txt="label", init_color="", label_width_ratio=2, 
                **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.set_variables()
        self.set_widgets(label_width_ratio)
        self.pack_widgets()
        self.set_init(label_txt, init_color)

    def set_variables(self):
        self.label = tk.StringVar()

    def set_widgets(self, label_width):
        self.w = OrderedDict()
        self.w["Label"] = tk.Label(self, textvariable=self.label, width=label_width, font=self.font)
        self.w["ColorSelector"] = sf.ColorSelector(self, width=10, height=10)
        
    def pack_widgets(self):
        for key, widget in self.w.items():
            f = tk.Y if key == "Label" else tk.BOTH
            e = False if key == "Label" else True
            widget.pack(side=tk.LEFT, fill=f, expand=e)

    def set_init(self, label_txt, init_color):
        self.set(init_color)
        self.label.set(label_txt)

    def set(self, color):
        self.w["ColorSelector"].set(color)

    def get(self):
        return self.w["DateInputBox"].get()

    def get_as_hex(self):
        return self.w["DateInputBox"].get_as_hex()


class InputListArea(tk.Frame):
    def __init__(self, master, input_rows, label_width, **kwargs):
        """
        input_rows = {label_text: [type, items]}
        type: combobox => items = (initial value, [combobox item list], state)
        type: date     => items = (initial value, press_enter_callback)
        type: color    => items = (initial value)
        """
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font

        self.set_variables()
        self.set_widgets(input_rows, label_width)
        self.pack_widgets()
        self.set_init()

    def set_variables(self):
        pass

    def set_widgets(self, input_rows, label_width):
        self.w = OrderedDict()
        for label_txt, (item_type, items) in input_rows.items():
            if item_type == "combobox":
                self.w[label_txt] = LabelCombo(self, 
                                               label_txt=label_txt, 
                                               init_txt=items[0], 
                                               combo_list=items[1],
                                               state=items[2],
                                               label_width_ratio=label_width)
            elif item_type == "date":
                self.w[label_txt] = LabelDateInputBox(self, 
                                                      label_txt=label_txt,
                                                      init_date=items[0],
                                                      press_enter_callback=items[1],
                                                      label_width_ratio=label_width)
            elif item_type == "color":
                self.w[label_txt] = LabelColorSelector(self,
                                                       label_txt=label_txt,
                                                       init_color=items[0],
                                                       label_width_ratio=label_width)
            else:
                raise f"InputListArea not support type {item_type}"

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
    
    def get_as_hex(self, k):
        return self.w[k].get_as_hex()