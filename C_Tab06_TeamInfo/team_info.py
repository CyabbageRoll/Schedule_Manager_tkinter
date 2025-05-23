# default
from collections import OrderedDict
import tkinter as tk
# additional
import pandas as pd
# user
import D_SubFrames as sf


class TeamInfo(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.OB = master.OB
        self.members = [self.SP.user] + [m for m in self.SP.members if m != self.SP.user]
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["info1"] = tk.Text(self, font=self.font)
        self.w["info2"] = tk.Text(self, font=self.font)
        self.w["info3"] = tk.Text(self, font=self.font)
        self.w["info4"] = tk.Text(self, font=self.font)

    def pack_widgets(self):
        self.w["info1"].place(relx=0.01, rely=0.01, relwidth=0.49, relheight=0.49)
        self.w["info2"].place(relx=0.51, rely=0.01, relwidth=0.49, relheight=0.49)
        self.w["info3"].place(relx=0.01, rely=0.51, relwidth=0.49, relheight=0.49)
        self.w["info4"].place(relx=0.51, rely=0.51, relwidth=0.49, relheight=0.49)

    def refresh(self):
        self.txt_update_config("normal")
        self.set_info1()
        self.set_info2()
        self.set_info3()
        self.set_info4()
        self.txt_update_config("disable")

    def txt_update_config(self, state):
        for key in self.w:
            self.w[key].configure(state=state)

    def set_init(self):
        self.refresh()

    def set_bind(self):
        pass

    def set_new_text(self, info_idx, txt):
        self.w[f"info{info_idx}"].delete("1.0", tk.END)
        self.w[f"info{info_idx}"].insert(tk.END, txt)

    def set_info1(self):
        txt = "working hours\n"
        txt = "Name : Begin ~ End [Working hours] (Breaks) : \n"
        for user_name in self.members:
            txt += f"\n{user_name:12s} : {self.fetch_working_hours(user_name)} {self.fetch_work_place(user_name)} : {self.fetch_info_overwork(user_name)}"
        self.set_new_text(1, txt)

    def fetch_working_hours(self, user_name):
        df_idx = str(self.OB["Date"]) + "-" + user_name
        if df_idx not in self.SD["daily_sch"].index:
            return ""
        
        ds = self.SD["daily_sch"].loc[df_idx, ["CTOTAL", "CFROM", "CTO", "CBREAK"]]
        if not ds["CTOTAL"]:
            return ""
        
        work_from = f'{ds["CFROM"][1:3]}:{ds["CFROM"][3:]}'
        work_to = f'{ds["CTO"][1:3]}:{ds["CTO"][3:]}'
        return f" {work_from} ~ {work_to}  [{ds['CTOTAL']}h] ({ds['CBREAK']}h)"

    def fetch_info_overwork(self, user_name):
        df_idx = str(self.OB["Date"]) + "-" + user_name
        if df_idx not in self.SD["daily_info"].index:
            return ""
        overwork = self.SD["daily_info"].loc[df_idx, "OverWork"]
        if overwork != overwork or overwork == "None":
            return ""
        return f": {overwork}"

    def fetch_work_place(self, user_name):
        df_idx = str(self.OB["Date"]) + "-" + user_name
        if df_idx not in self.SD["daily_info"].index:
            return "< >"
        work_place = self.SD["daily_info"].loc[df_idx, "Work_Place"]
        if work_place != work_place or work_place == "None":
            return "< >"
        return f"<{work_place}>"

    def set_info2(self):
        txt = "information:\n"
        info2_dicts = {user_name: self.fetch_info2(user_name)for user_name in self.members}
        info2_keys = self.fetch_info2_keys()
        for info2_key in info2_keys:
            txt += f"{info2_key}:\n"
            for member_name, info2_dic in info2_dicts.items():
                txt += f"\t{member_name:15s}: {info2_dic.get(info2_key, '')}\n"
            txt += "\n"
        self.set_new_text(2, txt)

    def fetch_info2_keys(self):
        return ["Health", "Safety", "Info1", "Info2", "Info3"]

    def fetch_info2(self, user_name):
        df_idx = str(self.OB["Date"]) + "-" + user_name
        if df_idx not in self.SD["daily_info"].index:
            return {}
        ds_info = self.SD["daily_info"].loc[df_idx, :]
        info_dic = {}
        info2_keys = self.fetch_info2_keys()
        for idx in info2_keys:
            if ds_info[idx] and ds_info[idx] == ds_info[idx]:
                info_dic[idx] = ds_info[idx]
        return info_dic

    def set_info3(self):
        txt = "info3"
        self.set_new_text(3, txt)

    def set_info4(self):
        txt = "info4"
        self.set_new_text(4, txt)