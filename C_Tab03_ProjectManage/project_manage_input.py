# default
from collections import OrderedDict
import tkinter as tk
import datetime
# additional
import pandas as pd
# user
import D_SubFrames as sf
import A_DataSettingRW as DS


class ProjectManageInput(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.class_list=["Project1", "Project2", "Project3", "Project4", "Task", "Ticket"]
        self.class2idx = {c: i for i, c in enumerate(self.class_list)}
        self.parent_idx = None
        self.subject_init = " PPP Editor "
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["Text"] = tk.Label(self, text=" ", font=self.font)
        self.w["Text1"] = tk.Label(self, text="Editor", font=self.font)
        self.w["Text2"] = tk.Label(self, text=" ", font=self.font)

        # self.w["Name"] = sf.LabelCombo(self, label_txt="Name", label_width=20)
        self.w["Name"] = sf.LabelEntryBox(self, label_txt="Name", label_width=20, input_type="str")
        self.w["Owner"] = sf.LabelCombo(self, label_txt="Owner", label_width=20, state="readonly",
                                        combo_list=[self.SP.user] + self.SP.members)
        self.w["Status"] = sf.LabelCombo(self, label_txt="Status", label_width=20, state="readonly",
                                         combo_list=["ToDo", "Done", "Cancel", "Regularly"])
        self.w["OrderValue"] = sf.LabelEntryBox(self, label_txt="OrderValue", label_width=20, input_type="float")
        self.w["Parent_ID"] = sf.LabelCombo(self, label_txt="Parent ID", label_width=20, state="disable")
        self.w["Parent_Name"] = sf.LabelCombo(self, label_txt="Parent Name", label_width=20, state="disable")
        self.w["Plan_Begin_Date"] = sf.LabelDateInputBox(self, label_txt="Plan Begin Date", label_width=20)
        self.w["Plan_End_Date"] = sf.LabelDateInputBox(self, label_txt="Plan End Date", label_width=20)
        self.w["Total_Estimate_Hour"] = sf.LabelEntryBox(self, label_txt="Plan Hour", label_width=20, input_type="float")
        self.w["Actual_Begin_Date"] = sf.LabelCombo(self, label_txt="Actual Begin Date", label_width=20, state="disable")
        self.w["Actual_End_Date"] = sf.LabelCombo(self, label_txt="Actual End Date", label_width=20, state="disable")
        self.w["Actual_Hour"] = sf.LabelCombo(self, label_txt="Actual Hour", label_width=20, state="disable")
        self.w["Color"] = sf.LabelColorSelector(self, label_txt="Color", label_width=20)
        self.w["Goal"] = sf.LabelEntryBox(self, label_txt="Goal", label_width=20, input_type="str")
        self.w["Difficulty"] = sf.LabelEntryBox(self, label_txt="Difficulty", label_width=20, input_type="str")
        self.w["Num_Active_Children"] = sf.LabelCombo(self, label_txt="Num Active Children", label_width=20, state="disable")
        self.w["Last_Update"] = sf.LabelCombo(self, label_txt="Last Update", label_width=20, state="disable")
        self.w["Memo_label"] = tk.Label(self, text="Memo", font=self.font)
        self.w["Memo"] = tk.Text(self, font=self.font)

    def pack_widgets(self):
        for k, widget in self.w.items():
            widget.pack(side=tk.TOP, fill=tk.X, expand=False)

    def pack_forget_widgets(self):
        for k, widget in self.w.items():
            widget.pack_forget()

    def set_init(self):
        self.w["Text1"]["text"] = self.subject_init.replace("PPP", "")
        self.set((None, None), None, None)

    def set_bind(self):
        pass

    def update_input_box(self, ds, class_id):
        for k, v in ds.items():
            if k in self.w.keys():
                if k == "Memo":
                    self.w["Memo"].insert(0.0, v)
                else:
                    self.w[k].set(v)

        self.w["Parent_Name"].set(self.parent_name)
        p = self.class_list[class_id]
        self.w["Text1"]["text"] = self.subject_init.replace("PPP", p)
        
    def set(self, parent, selected_class, idx):
        self.parent_idx, self.parent_name = parent
        if selected_class:
            class_id = self.class2idx[selected_class]
            if idx:
                ds = self.SD[class_id + 1].loc[idx, :]
            else:
                ds = DS.create_initial_data_series(self.SP.user)
                ds["Parent_ID"] = self.parent_idx
            self.update_input_box(ds, class_id)

    def get(self):
        ds = DS.create_initial_data_series(self.w["Owner"].get())
        for k in ds.index:
            if k == "Memo":
                ds[k] = self.w[k].get("1.0", "end")
            elif k in self.w.keys():
                ds[k] = self.w[k].get()
        return ds