from collections import OrderedDict
import tkinter as tk
from tkinter import ttk

import D_SubFrames as sf


class LabelBoxBase(tk.Frame):
    def __init__(self, master, label_txt, init_value="", label_width=2, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.label_txt = label_txt
        self.label_width = label_width
        self.init_value = init_value
        self.w = OrderedDict()

    def initialize(self):
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_label(self.label_txt)
        self.set(self.init_value)
        self.set_bind()

    def set_variables(self):
        self.label = tk.StringVar()
        self.value = tk.StringVar()

    def set_widgets(self):
        self.w["Label"] = tk.Label(self, 
                                   textvariable=self.label,
                                   width=self.label_width,
                                   font=self.font)

    def pack_widgets(self):
        for key, widget in self.w.items():
            f = tk.Y if key == "Label" else tk.BOTH
            e = False if key == "Label" else True
            widget.pack(side=tk.LEFT, fill=f, expand=e)

    def set_label(self, label_txt):
        self.label.set(label_txt)

    def set(self, value):
        self.value.set(value)

    def get(self):
        return self.value.get()

    def set_bind(self):
        pass


class LabelCombo(LabelBoxBase):
    def __init__(self, master, label_txt="label_txt", init_value="", state="normal", combo_list=[], **kwargs):
        super().__init__(master, label_txt, init_value, **kwargs)
        self.state = state
        self.combo_list = combo_list
        self.initialize()

    def set_widgets(self):
        super().set_widgets()
        self.w["Box"] = ttk.Combobox(self,
                                     textvariable=self.value,
                                     values=self.combo_list,
                                     width=10,
                                     height=10,
                                     font=self.font,
                                     state=self.state)

    def set_list(self, combo_list):
        self.w["Box"]["values"] = combo_list

    def get_list(self):
        return self.w["Box"]["values"]
    
    def get(self):
        return self.w["Box"].get()


class LabelDateInputBox(LabelBoxBase):
    def __init__(self, master,
                 label_txt="label", init_value="", focus_out_callback=None, **kwargs):
        super().__init__(master, label_txt, init_value, **kwargs)
        self.callback = focus_out_callback
        self.initialize()

    def set_widgets(self):
        super().set_widgets()
        self.w["Box"] = sf.DateInputBox(self, 
                                        press_enter_callback=self.callback,
                                        width=10, height=10)

    def set(self, date):
        self.w["Box"].set(date)

    def get(self):
        return self.w["Box"].get()


class LabelColorSelector(LabelBoxBase):
    def __init__(self, master,
                 label_txt="label", init_value="", **kwargs):
        super().__init__(master, label_txt, init_value, **kwargs)
        self.initialize()

    def set_widgets(self):
        super().set_widgets()
        self.w["Box"] = sf.ColorSelector(self, width=10, height=10)

    def set(self, date):
        self.w["Box"].set(date)

    def get(self):
        return self.w["Box"].get()

    def set(self, color):
        self.w["Box"].set(color)

    def get(self):
        return self.w["Box"].get()

    def get_as_hex(self):
        return self.w["Box"].get_as_hex()


class LabelEntryBox(LabelBoxBase):
    def __init__(self, master, label_txt="label_txt", init_value="", 
                 justify=tk.LEFT, input_type="str",
                 **kwargs):
        super().__init__(master, label_txt, init_value, **kwargs)
        self.justify = justify
        supported_type = ["str", "int", "float", "list_str", "list_int"]
        assert input_type in supported_type, f"{input_type} is not supported"
        self.input_type = input_type
        self.bind_func_return_callback = None
        self.bind_func_focus_out_callback = None
        self.initialize()


    def set_widgets(self):
        super().set_widgets()
        self.w["Box"] = tk.Entry(self, 
                                 textvariable=self.value,
                                 justify=self.justify,
                                 width=10,
                                 font=self.font)
        
    def set_bind(self):
        # self.w["Box"].bind("<Return>", self.warning_type_miss_match)
        # self.w["Box"].bind("<FocusOut>", self.warning_type_miss_match)
        self.w["Box"].bind("<Return>", self.bind_func_return)
        self.w["Box"].bind("<FocusOut>", self.bind_func_focus_out)

    def warning_type_miss_match(self, event):
        if self.type_check():
            # self.w["Box"].configure(bg="SystemButtonFace")
            self.w["Box"].configure(bg="LightGrey")
        else:
            self.w["Box"].configure(bg="red")

    def bind_func_return(self, event):
        self.warning_type_miss_match(event)
        if self.bind_func_return_callback is not None:
            self.bind_func_return_callback()

    def bind_func_focus_out(self, event):
        self.warning_type_miss_match(event)
        if self.bind_func_focus_out_callback is not None:
            self.bind_func_focus_out_callback()

    def type_check(self):
        if self.input_type == "str":
            ret = True
        elif self.input_type == "int":
            ret = self.is_type_int()
        elif self.input_type == "float":
            ret = self.is_type_float()
        elif self.input_type == "list_str":
            ret = self.is_type_list_str()
        elif self.input_type == "list_int":
            ret = self.is_type_list_int()
        return ret

    def is_type_str(self):
        return True
    
    def is_type_int(self):
        try:
            int(self.get())
            return True
        except:
            return False

    def is_type_float(self):
        try:
            float(self.get())
            return True
        except:
            return False

    def is_type_list_str(self):
        try:
            [str(s) for s in self.get().split(",")]
            return True
        except:
            return False
        
    def is_type_list_int(self):
        try:
            [int(s) for s in self.get().split(",")]
            return True
        except:
            return False
        
    def get(self):
        return self.w["Box"].get()
    
    def set(self, str):
        self.value.set(str)


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
                                               init_value=items[0], 
                                               combo_list=items[1],
                                               state=items[2],
                                               label_width=label_width)
            elif item_type == "date":
                self.w[label_txt] = LabelDateInputBox(self, 
                                                      label_txt=label_txt,
                                                      init_value=items[0],
                                                      focus_out_callback=items[1],
                                                      label_width=label_width)
            elif item_type == "color":
                self.w[label_txt] = LabelColorSelector(self,
                                                       label_txt=label_txt,
                                                       init_value=items[0],
                                                       label_width=label_width)
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
        self.w[k].w["Box"]["values"] = l

    def get_list(self, k):
        return self.w[k].w["Box"]["values"]
    
    def get_as_hex(self, k):
        return self.w[k].get_as_hex()