# default
from collections import OrderedDict
import tkinter as tk
# additional
import pandas as pd
# user
import SubFrames as sf
import DataSettingRW as DS


class ProjectManage(tk.Frame):
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
        self.w["Selector"] = sf.ProjectSelector(self)
        buttons = [["Create", self.db_create],
                   ["Update", self.db_update],
                   ["Delete", self.db_delete]]
        self.w["ButtonRow"] = sf.ButtonRow(self, buttons)
        self.w["Input"] = sf.ProjectManageInput(self)

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

    def db_create(self):
        ds, type_warning = self.get_item_and_type_warning()
        if type_warning:
            print(type_warning)
        else:
            self.update_schedule_data(ds)
        self.update_display_items()

    def db_update(self):
        print("press update")

    def db_delete(self):
        print("press delete")

    def get_item_and_type_warning(self):
        ds = self.w["Input"].get()
        ds, type_warning = DS.ds_type_converter(ds)
        return ds, type_warning

    def update_schedule_data(self, ds):
        (parent_idx, parent_name), selected_class, idx = self.w["Selector"].get()
        prj_id = self.w["Selector"].class2idx[selected_class] + 1
        self.SD[prj_id].loc[ds.name] = ds
        self.logger.info(f"insert schedule data {ds.name}")

    def is_correct_data(self):
        # 名前のダブりないか？
        # 予定工数が入力されているか？
        # 親プロジェクトはあるか？
        pass

    def update_display_items(self):
        self.w["Selector"].update_list_box()