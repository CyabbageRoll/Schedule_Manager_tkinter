# default
from collections import OrderedDict
import tkinter as tk
from tkinter import messagebox
import datetime
# additional
import pandas as pd
# user
import D_SubFrames as sf
import A_DataSettingRW as DS
import C_Tab03_ProjectManage as tab3


class ProjectManage(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.OB = master.OB
        self.add_bind_func = None
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
        buttons = [["Create", self.db_create],
                   ["Update", self.db_update],
                   ["Delete", self.db_delete]]
        self.w["ButtonRow"] = sf.ButtonRow(self, buttons)
        self.w["Input"] = tab3.ProjectManageInput(self)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = True if k != "ButtonRow" else False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def set_init(self):
        self.w["Selector"].call_back_changed = self.project_select_changed
        self.w["Selector"].prj_select_changed(None, 0)

    def project_select_changed(self, parent, selected_class, idx):
        self.w["Input"].set(parent, selected_class, idx)
        if idx is None:
            self.w["ButtonRow"].w["Create"].config(state=tk.NORMAL)
            self.w["ButtonRow"].w["Update"].config(state=tk.DISABLED)
            self.w["ButtonRow"].w["Delete"].config(state=tk.DISABLED)
        else:
            self.w["ButtonRow"].w["Create"].config(state=tk.DISABLED)
            self.w["ButtonRow"].w["Update"].config(state=tk.NORMAL)
            self.w["ButtonRow"].w["Delete"].config(state=tk.NORMAL)

    def set_bind(self):
        pass

    def update_func(self):
        if self.add_bind_func is not None:
            self.add_bind_func()

    def db_create(self):
        flag, items = self.get_correct_data_or_warning_msg()
        if not flag:
            return
        else:
            ds, _, class_idx = items
            self.update_schedule_data(ds, class_idx)
            self.update_display_items()
        self.update_func()

    def db_update(self):
        flag, items = self.get_correct_data_or_warning_msg()
        if not flag:
            return
        else:
            ds, _, class_idx = items
            (_, _), _, ds.name = self.w["Selector"].get()
            self.update_schedule_data(ds, class_idx)
            self.update_display_items()
        self.update_func()

    def db_delete(self):
        _, _, class_idx, current_idx = self.get_item_and_type_warning()
        if self.SD[class_idx].loc[current_idx, "Actual_Hour"] > 0:
            messagebox.showinfo("Information", "Unable to delete because actual hour is not Zero")
            return
        if class_idx < 6:
            p_ids = self.SD[class_idx+1]["Parent_ID"].tolist()
            if current_idx in p_ids:
                messagebox.showinfo("Information" ,"Unable to delete because project have children")
                return
        self.SD[class_idx].loc[current_idx, "Status"] = "Deleted"
        self.SD[class_idx].loc[current_idx, "Last_Update"] = datetime.datetime.today().strftime("%Y-%m-%d")
        self.w["Selector"].clear_button_press()
        self.update_func()

    def print_type_warning(self, type_warning):
        msg = ""
        for k, v in type_warning.items():
            msg += f"{k} : {v}\n"
        messagebox.showinfo("Information", msg)

    def get_item_and_type_warning(self):
        ds = self.w["Input"].get()
        ds, type_warning = DS.ds_type_converter(ds)
        (_, _), selected_class, current_idx = self.w["Selector"].get()
        class_idx = self.w["Selector"].class2idx[selected_class] + 1
        return ds, type_warning, class_idx, current_idx

    def update_schedule_data(self, ds, class_idx):
        ds["Last_Update"] = datetime.datetime.today().strftime("%Y-%m-%d")
        self.SD[class_idx].loc[ds.name] = ds
        pid = ds["Parent_ID"]

        df = self.SD[class_idx]
        indices = df[df["Parent_ID"] == pid].index
        orders = df.loc[indices, "OrderValue"]
        orders = orders.sort_values()
        for order, idx in enumerate(orders.index):
            self.SD[class_idx].loc[idx, "OrderValue"] = order
            self.SD[class_idx].loc[idx, "Last_Update"] = datetime.datetime.today().strftime("%Y-%m-%d")
        self.logger.info(f"insert schedule data {ds.name}")

    def get_correct_data_or_warning_msg(self):
        ds, type_warning, class_idx, current_idx = self.get_item_and_type_warning()
        if type_warning:
            self.print_type_warning(type_warning)
            return False, ()
        correct, msg = self.is_correct_name_hour_parent(ds, class_idx, current_idx)
        if not correct:
            messagebox.showinfo("Information", msg)
            return False, ()
        return True, (ds, type_warning, class_idx)

    def is_correct_name_hour_parent(self, ds, class_idx, current_idx):
        if not self.is_name_unique(ds, class_idx, current_idx):
            return False, "Name is not unique"
        if not self.is_not_hour_zero(ds, class_idx):
            return False, "estimate hour is Zero"
        if not self.exists_parent(ds, class_idx):
            return False, "parent does not exist"
        return True, "OK"

    def is_name_unique(self, ds, class_idx, current_idx):
        df = self.SD[class_idx]
        if class_idx == 6:
            # Ticketの場合はownerが違えばチケット名の重複を許す
            df = df[df["Owner"] == ds["Owner"]]
            names = df[df["Parent_ID"] == ds["Parent_ID"]]["Name"].tolist()
        else:
            names = df[df["Parent_ID"] == ds["Parent_ID"]]["Name"].tolist()
        # 更新で名前が変わっていない
        if current_idx:
            if ds["Name"] == df.loc[current_idx, "Name"]:
                return True
        # 名前がすでに入っている
        if ds["Name"] in names:
            return False
        return True

    def is_not_hour_zero(self, ds, class_idx):
        if class_idx != 6:
            return True
        if ds["Total_Estimate_Hour"] > 0:
            return True
        return False

    def exists_parent(self, ds, class_idx):
        p_id = ds["Parent_ID"]
        if p_id == "0":
            return True
        if p_id in self.SD[class_idx-1].index.tolist():
            return True
        return False

    def update_display_items(self):
        self.w["Selector"].update_list_box()

    def set(self, class_idx, idx):
        self.w["Selector"].set(class_idx, idx)