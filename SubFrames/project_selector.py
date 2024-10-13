# default
from collections import OrderedDict
import tkinter as tk
# additional
import pandas as pd
# user
import SubFrames as sf


class ProjectSelector(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.ids = [None] * 6
        self.class_list=["Project1", "Project2", "Project3", "Project4", "Task", "Ticket"]
        self.class_dict = {f"P{i}": c for i, c in enumerate(self.class_list)}
        self.class2idx = {c: i for i, c in enumerate(self.class_list)}
        self.changed = self.tmp
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        pass

    def set_widgets(self):
        self.w1 = OrderedDict()
        self.w1["Space0"] = tk.Label(self, text="", font=self.font)
        self.w1["Text1"] = tk.Label(self, text="⭐️⭐️⭐️⭐️⭐️ Select Item Class ⭐️⭐️⭐️⭐️⭐️", font=self.font)
        self.w1["Space1"] = tk.Label(self, text="", font=self.font)
        self.w1["Class_selector"] = sf.LabelCombo(self,
                                                  label_txt="Select Class",
                                                  label_width=20,
                                                  init_txt="Project1",
                                                  state="readonly",
                                                  combo_list=self.class_list)

        # PROJECT
        self.w1["Space2"] = tk.Label(self, text="", font=self.font)
        self.w1["Text3"] = tk.Label(self, text="Select Parent", font=self.font)
        for k, c in self.class_dict.items():
            self.w1[k] = sf.LabelCombo(self, label_txt=c, label_width=20, state="readonly")

        self.w2 = OrderedDict()
        self.w2["Text1"] = tk.Label(self, text="")
        self.w2["Text2"] = tk.Label(self, text="Select if Update", font=self.font)
        
        self.w3 = OrderedDict()
        self.w3["Idx"] = sf.LabelCombo(self, label_txt="index", label_width=20, state="disabled")

    def pack_widgets(self):
        selected_class = self.w1["Class_selector"].get()
        for k, widget in self.w1.items():
            if self.class_dict.get(k, None) == selected_class:
                prj_k = k
                break
            widget.pack(side=tk.TOP, fill=tk.X, expand=False)
        for k, widget in self.w2.items():
            widget.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.w1[prj_k].pack(side=tk.TOP, fill=tk.X, expand=False)
        self.w3["Idx"].pack(side=tk.TOP, fill=tk.X, expand=False)

    def pack_forget_widgets(self):
        for w in [self.w1, self.w2, self.w3]:
            for k, widget in w.items():
                widget.pack_forget()

    def set_init(self):
        self.update_list_box()
        self.update_idx()

    def set_bind(self):
        self.w1["Class_selector"].w["Combobox"].bind("<<ComboboxSelected>>", self.class_select_changed)
        # for文にすると、lambda式の中の番号がうまくいかない
        self.w1[f"P0"].w["Combobox"].bind("<<ComboboxSelected>>", lambda x: self.prj_select_changed(x, 0))
        self.w1[f"P1"].w["Combobox"].bind("<<ComboboxSelected>>", lambda x: self.prj_select_changed(x, 1))
        self.w1[f"P2"].w["Combobox"].bind("<<ComboboxSelected>>", lambda x: self.prj_select_changed(x, 2))
        self.w1[f"P3"].w["Combobox"].bind("<<ComboboxSelected>>", lambda x: self.prj_select_changed(x, 3))
        self.w1[f"P4"].w["Combobox"].bind("<<ComboboxSelected>>", lambda x: self.prj_select_changed(x, 4))
        self.w1[f"P5"].w["Combobox"].bind("<<ComboboxSelected>>", lambda x: self.prj_select_changed(x, 5))

    # 表示するComboboxを変更する
    def class_select_changed(self, event):
        self.pack_forget_widgets()
        self.pack_widgets()
        self.update_idx()

    def prj_select_changed(self, event, idx):
        self.reset_values(idx)
        self.reset_list_box()
        self.update_list_box()
        self.update_idx()

    def reset_list_box(self):
        for i in range(6):
            self.w1[f"P{i}"].w["Combobox"]["values"] = []

    def reset_values(self, idx):
        for i in range(idx+1, 6):
            self.w1[f"P{i}"].set("")

    def update_list_box(self):
        self.find_prj_ids_from_input()
        for i, idx in enumerate(["0"] + self.ids[:-1]):
            if idx:
                name_list = self.SD[i+1][self.SD[i+1]["Parent_ID"] == idx]["Name"].tolist()
                self.w1[f"P{i}"].w["Combobox"]["values"] = name_list

    def find_prj_ids_from_input(self):
        idx = "0"
        for i in range(6):
            prj = self.w1[f"P{i}"].get()
            idx = self.specify_prj_idx(self.SD[i+1], prj, idx)
            self.ids[i] = idx

    def specify_prj_idx(self, df, prj, p_id):
        if p_id:
            # prj名と親IDから自分のidxを特定する
            df = df[df.iloc[:, 1] == p_id]
            idx = df.index[df.iloc[:, 0] == prj]
            idx = idx[0] if len(idx) else None
        else:
            idx = None
        return idx
    
    def update_idx(self):
        _, _, idx = self.get()
        self.w3["Idx"].set(idx)
        self.item_changed()

    def get(self):
        selected_class = self.w1["Class_selector"].get()
        i = self.class2idx[selected_class]
        idx = self.ids[i]
        tmp = ["0"] + self.ids
        parent_idx = tmp[i]
        if i:
            parent_name = self.w1[f"P{i-1}"].get()
        else:
            parent_name = None
        return (parent_idx, parent_name), selected_class, idx
    
    def item_changed(self):
        parent, selected_class, idx = self.get()
        self.changed(parent, selected_class, idx)

    def tmp(self, p, s, i):
        pass