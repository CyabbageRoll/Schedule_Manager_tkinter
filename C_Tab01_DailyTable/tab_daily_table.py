from collections import OrderedDict, defaultdict
import datetime
import tkinter as tk
from tkinter import messagebox
import pandas as pd

import D_SubFrames as sf

class DailyInformation(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.OB = master.OB
        self.column_name_list = [f"C{i//4:02d}{(i%4)*15:02d}" for i in range(24*4)]
        self.daily_schedule_update_bind = None
        self.daily_info_update_bind = None
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()
        self.logger.debug("initialized Daily Table Tab")

    def set_variables(self):
        columns = ["Time", "Schedule", "Import"]
        rows = {i: [self.row_id_to_daily_time(i), "", ""] for i in range(24*4)}
        self.df = pd.DataFrame.from_dict(data=rows, columns=columns, orient="index")

    def row_id_to_daily_time(self, row_id):
        if row_id % 4:
            t = f"{' ':12s} ~ {(row_id+1)//4:02d} : {((row_id+1)%4)*15:02d}"
        else:
            t = f"{row_id//4:02d} : {(row_id%4)*15:02d} ~ {(row_id+1)//4:02d} : {((row_id+1)%4)*15:02d}"
        return t

    def set_widgets(self):
        self.w = OrderedDict()
        input_rows = {}
        for k in self.SD["daily_info"].columns[1:]:
            input_rows[k] = ["combobox", ["", [], "normal"]]
        self.w["Info_area"] = sf.InputListArea(self, input_rows=input_rows, label_width=12)
        # 入力した予定の取り消し
        self.w["Buttons"] = sf.ButtonRow(self, buttons=[["Free", self.delete_item]])
        # 1日の予定入力欄
        self.w["table"] = sf.ScrollableTable(self, df=self.df, widths=[100, 250, 250])

    def pack_widgets(self):
        self.w["Info_area"].pack(side=tk.TOP, fill=tk.X, expand=False)
        self.w["Buttons"].pack(side=tk.TOP, fill=tk.X, expand=False)
        self.w["table"].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def set_init(self):
        self.refresh()

    def selection(self):
        return self.w["table"].selection()

    def update_item(self, ds):
        self.logger.debug("Try to update daily table")
        rows = self.selection()
        if self.OB["Member"] != self.SP.user:
            self.logger.debug(f"selected member is {self.OB['Member']} different to user {self.SP.user}")
            return
        self.logger.debug(f"selected row is {rows}")
        if not rows:
            return

        rows = [int(row) for row in rows]
        update_dict = self.update_daily_sch(rows, ds)
        self.update_actual_hours(update_dict)
        items = self.update_local_df()
        self.update_table_items(items)
        self.daily_schedule_update_bind()

    def delete_item(self):
        ds = pd.Series([""], name="")
        self.update_item(ds)

    def update_daily_sch(self, rows, ds):
        # self.SDで保有しているdaily tableの更新(時間計算をする必要があるので、時間増分を計算)
        df_idx = self.generate_df_idx()
        cols = [self.column_name_list[row] for row in rows]
        current_item = self.SD["daily_sch"].loc[df_idx, cols]
        self.SD["daily_sch"].loc[df_idx, cols] = ds.name

        update_dict = defaultdict(float)
        update_dict[ds.name] = len(rows) * 0.25
        for idx in current_item:
            update_dict[idx] -= 0.25
        return update_dict

    def update_actual_hours(self, update_dict):
        for idx, h in update_dict.items():
            if idx == "" or h == 0:
                continue
            self.SD[6].loc[idx, "Actual_Hour"] += h

    def update_local_df(self):
        df_idx = self.generate_df_idx()
        if df_idx not in self.SD["daily_sch"].index:
            self.SD["daily_sch"].loc[df_idx, :] = ""
            self.SD["daily_sch"].loc[df_idx, "Owner"] = self.SP.user

        ds = self.SD["daily_sch"].loc[df_idx, :]
        items = [["", "", "", ""] for _ in range(24*4)]
        for i in range(24*4):
            idx = ds.iloc[i+1]
            if not idx:
                continue
            item_name = self.SD[6].loc[idx, "Name"]
            info = self.get_item_info(idx)
            color = self.SD[6].loc[idx, "Color"]
            items[i] = (idx, item_name, info, color)

        current_idx = ""
        same_count = 0
        for i in range(24*4):
            previous_idx = current_idx
            current_idx = items[i][0]
            if not current_idx:
                self.df.iloc[i, 1] = ""
                continue
            
            if previous_idx != current_idx:
                same_count = 0
        
            if same_count == 0:
                self.df.iloc[i, 1] = items[i][2] + items[i][1]
            if same_count == 1:
                self.df.iloc[i-1, 1] = items[i][2]
                self.df.iloc[i, 1] = items[i][1]
            if same_count > 1:
                self.df.iloc[i, 1] = "↑"
            same_count += 1

        return items

    def get_item_info(self, idx):
        info = []
        for i in range(3):
            p_name, idx = self.SD[6 - i].loc[idx, ["Name", "Parent_ID"]]
            info.append(p_name)
        info = info[-1:0:-1]
        info = "-".join(info)
        return info

    def update_table_items(self, items):
        for row in range(24*4):
            self.w["table"].update_cell(index=row, column="Schedule", value=self.df.iloc[row, 1])
            idx, _, _, color = items[row]
            if idx:
                self.w["table"].set_cell_color(row, color=color)
            else:
                self.w["table"].set_cell_color(row, color="base")

    def refresh(self):
        self.logger.debug("refresh")
        items = self.update_local_df()
        self.update_table_items(items)
        self.set_info_values()
        self.calc_working_hours()

    def set_bind(self):
        for k in self.SD["daily_info"].columns[1:]:
            self.w["Info_area"].w[k].w["Box"].bind("<Return>", lambda x, k=k: self.info_item_update_bind_func(k, x))
            self.w["Info_area"].w[k].w["Box"].bind("<FocusOut>", lambda x, k=k: self.info_item_update_bind_func(k, x))

    def info_item_update_bind_func(self, k, event):
        if self.OB["Member"] != self.SP.user:
            messagebox.showinfo("Information", "You can't update other member's information")
            return
        txt = self.w["Info_area"].w[k].get()
        df_idx = self.generate_df_idx()
        self.SD["daily_info"].loc[df_idx, k] = txt
        self.SD["daily_info"].loc[df_idx, "Owner"] = self.SP.user
        self.daily_info_update_bind()

    def generate_df_idx(self):
        return str(self.OB["Date"]) + "-" + self.OB["Member"]
    
    def set_info_values(self):
        df_idx = self.generate_df_idx()
        for k in self.SD["daily_info"].columns[1:]:
            v = self.SD["daily_info"].loc[df_idx, k] if df_idx in self.SD["daily_info"].index else ""
            if v == v and v is not None:
                self.w["Info_area"].set(k, v)
            else:
                self.w["Info_area"].set(k, "")


    def calc_working_hours(self):
        df_idx = self.generate_df_idx()
        if df_idx not in self.SD["daily_sch"].index:
            return
        ds = self.SD["daily_sch"].loc[df_idx, :]
        working_hours, working_break = 0, 0
        working_from, working_to_idx = "", 0
        break_tmp = 0
        for i, dddd in enumerate(self.column_name_list):
            if ds[dddd]:
                working_hours += 0.25
                working_break += break_tmp
                break_tmp = 0
                working_to_idx = i
                if not working_from:
                    working_from = dddd
            elif working_from:
                break_tmp += 0.25
        if working_hours:
            working_to_idx = working_to_idx + 1 if working_to_idx + 1 < len(self.column_name_list) else 0
            self.SD["daily_sch"].loc[df_idx, "CTOTAL"] = working_hours
            self.SD["daily_sch"].loc[df_idx, "CFROM"] = working_from
            self.SD["daily_sch"].loc[df_idx, "CTO"] = self.column_name_list[working_to_idx]
            self.SD["daily_sch"].loc[df_idx, "CBREAK"] = working_break
        