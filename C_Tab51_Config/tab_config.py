# default
from collections import OrderedDict
import tkinter as tk
from dataclasses import fields, field
from typing import List

# user
import D_SubFrames as sf

class ConfigTable(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.GP = master.GP
        self.OB = master.OB
        self.MEMO = master.MEMO
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        self.msg = tk.StringVar()
        self.section_label = {0: "Parameter Configs",
                              1: "GUI Configs"}
        self.type_dict = {str: "str", 
                          int: "int", 
                          float: "float", 
                          List[str]: "list_str",
                          list: "list_str",}
        self.explanation_dict = {"members": "表示メンバー名",}

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["Label"] = tk.Label(self, textvariable=self.msg, font=self.font, anchor="w")
        self.w["Buttons"] = sf.ButtonRow(self,
                                         buttons=[["Set", self.button_save],
                                                  ["Load", self.button_load],
                                                  ])

        for i, params in enumerate([self.SP, self.GP]):
            self.w[f"Label{i}"] = tk.Label(self, text=self.section_label[i], font=self.font, anchor="w")
            for field in fields(params):
                item_name = field.name
                item_value = getattr(params, item_name)
                item_type = self.type_dict[field.type]
                display_name = self.explanation_dict.get(item_name, item_name)
                self.w[item_name] = sf.LabelEntryBox(self, 
                                                     label_txt=display_name,
                                                     init_value=item_value,
                                                     input_type=item_type,
                                                     label_width=30)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = True if k == "table" else False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def refresh(self):
        pass

    def set_init(self):
        self.refresh()

    def set_bind(self):
        pass

    def button_save(self):
        print(self.SP)
        for i, params in enumerate([self.SP, self.GP]):
            param_dict = vars(params)
            for key in param_dict:
                value = self.w[key].get()
                value_type = self.type_dict[type(param_dict[key])]
                converted_value = self.convert_type(value, value_type)
                if value_type in ["list_str", "list_int"]:
                    param_dict[key][:] = converted_value
                else:
                    param_dict[key] = converted_value

        self.logger.debug("Saved Configurations")
        print(self.SP)

    def button_load(self):
        for i, params in enumerate([self.SP, self.GP]):
            for field in fields(params):
                item_name = field.name
                self.w[item_name].set(getattr(params, item_name))
        self.logger.debug("Loaded Configurations")

    def convert_type(self, value, item_type):
        if item_type == "str":
            return str(value)
        elif item_type == "int":
            return int(value)
        elif item_type == "float":
            return float(value)
        elif item_type == "list_str":
            if value:
                return [str(s) for s in value.split(" ")]
            else:
                return []
        elif item_type == "list_int":
            if value:
                return [int(s) for s in value.split(" ")]
            else:
                return []
        else:
            raise ValueError(f"Unknown type: {item_type}")