# default
import random
from collections import OrderedDict
import tkinter as tk
import datetime
# additional
import pandas as pd
# user
from A_DataSettingRW import type_converter, serial_numbering, create_initial_data_series
import D_SubFrames as sf


class ATT(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.GP = master.GP
        self.click_apply_bind = None
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        self.msg = tk.StringVar()
        columns = ["Order", "Name", "Total_Estimate_Hour", "Plan_Begin_Date", "Plan_End_Date", "Actual_Hour"]
        rows = {i: [""]*len(columns) for i in range(1)}
        self.df = pd.DataFrame.from_dict(data=rows, columns=columns, orient="index")

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["label"] = tk.Label(self, textvariable=self.msg, font=self.font, anchor="w")
        self.w["selector"] = sf.ProjectSelector(self, update_item=False)
        self.w["button_apply"] = sf.ButtonRow(self,
                                              buttons=[["APPLY", self.button_apply]])
        self.w["table"] = sf.ScrollableTable(self, self.df)
        self.w["button_row"] = sf.ButtonRow(self,
                                            buttons=[["ADD", self.button_add],
                                                     ["DELETE", self.button_delete],
                                                     ["🔼", self.button_up],
                                                     ["🔽", self.button_down],
                                                     ["PULL", self.button_pull],
                                                     ])
        self.w["input"] = tk.Text(self, font=self.font)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = True if k == "table" else False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def set_init(self):
        self.w["selector"].call_back_changed = self.project_select_changed
        self.w["selector"].prj_select_changed(None, 0)

    def project_select_changed(self, parent, selected_class, idx):
        self.parent = parent
        self.msg.set(f"{parent=}, {selected_class=}, {idx=}")
        self.class_idx = self.w["selector"].class2idx[selected_class] + 1
        df = self.SD[self.class_idx]
        df = df[df["Parent_ID"] == parent[0]]
        df = df[["Order", "Name", "Total_Estimate_Hour", "Plan_Begin_Date", "Plan_End_Date", "Actual_Hour"]]
        self.update_table_contents(df)

    def update_order_numbers(self, df):
        orders = df.loc[:, "Order"]
        orders = orders.sort_values()
        for order, idx in enumerate(orders.index):
            df.loc[idx, "Order"] = int(order)
        df = df.sort_values("Order")
        return df

    def update_table_contents(self, df):
        df = self.update_order_numbers(df)
        self.w["table"].refresh(df)
        self.update_input_area()

    def update_input_area(self, user_txt_list=[""]):
        txt = ["新しい項目を追加するにはカンマ区切りで、名前, 工数, 開始日, 納期を入力してください。名前と工数は必須。開始日と納期はない場合は空白を入力してください。1行目(この行)は無視されます)"]
        txt += user_txt_list
        self.w["input"].delete('1.0', 'end')
        self.w["input"].insert("1.0", "\n".join(txt))

    def set_bind(self):
        pass

    def button_apply(self):
        df = self.w["table"].df
        if self.parent[0] == "0":
            color_dic = sf.generate_color_dict()
            color = random.choice(list(color_dic.keys()))
        else:
            color = self.SD[self.class_idx-1].loc[self.parent[0], "Color"]
        for idx in df.index:
            if idx not in self.SD[self.class_idx].index:
                # 新規アイテムは登録した情報を入れる
                ds = create_initial_data_series(self.SP.user)
                for col in df.columns:
                    ds[col] = df.loc[idx, col]
                ds["Color"] = color
                ds["Parent_ID"] = self.parent[0]
                self.SD[self.class_idx].loc[ds.name] = ds
            else:
                # すでにあるitemは順序、工数、納期、開始日のみを書き換える
                self.SD[self.class_idx].loc[idx, "Order"] = df.loc[idx, "Order"]
                self.SD[self.class_idx].loc[idx, "Total_Estimate_Hour"] = df.loc[idx, "Total_Estimate_Hour"]
                self.SD[self.class_idx].loc[idx, "Plan_Begin_Date"] = df.loc[idx, "Plan_Begin_Date"]
                self.SD[self.class_idx].loc[idx, "Plan_End_Date"] = df.loc[idx, "Plan_End_Date"]
        # update
        self.click_apply_bind()

    def button_add(self):
        inputs = self.w["input"].get("1.0", "end")
        inputs = inputs.split("\n")
        parse_inputs = [self.parse_string(s) for s in inputs[1:]]
        msg = []
        for inp, item in zip(inputs[1:], parse_inputs):
            if item is None:
                continue
            if item["Error"] is None:
                index = serial_numbering(self.SP.user)
                max_order = self.df.max(axis=0)["Order"]
                max_order = max_order if max_order else 0
                item["Order"] += int(max_order)
                for header in self.df.columns:
                    self.w["table"].update_cell(index, header, item[header])
            elif item["Error"] == "Name Exists":
                # 名前がすでにある場合
                df = self.w["table"].df
                index = df[df["Name"] == item["Name"]].index[0]
                for header in self.df.columns:
                    self.w["table"].update_cell(index, header, item[header])
            else:
                msg.append(inp + f" : {item['Error']}")
        msg.append("")
        self.update_input_area(user_txt_list=msg)

    def parse_string(self, s):
        default_values = [1, "", ""]
        s = [si.replace(" ", "") for si in s.split(",")]
        s = s + default_values[len(s)-1:]

        if not len(s):
            return
        if s[0] == "":
            return
        if s[1] == "":
            s[1] = 0.25

        item = {"Order": 1,
                "Name": s[0],
                "Total_Estimate_Hour": s[1],
                "Plan_Begin_Date": s[2],
                "Plan_End_Date": s[3],
                "Actual_Hour": 0,
                "Error": None}

        # 名前のダブりチェック
        names = self.w["table"].df["Name"].tolist()
        if item["Name"] in names:
            item["Error"] = "Name Exists"

        # 時間チェック
        ret, flag = type_converter(item["Total_Estimate_Hour"], float)
        if flag and ret > 0:
            item["Total_Estimate_Hour"] = ret
        else:
            item["Error"] = "工数が正しくありません"
            return item

        # 日付チェック
        tmp = sf.DateInputBox(self)
        for date_type in ["Plan_Begin_Date", "Plan_End_Date"]:
            if item[date_type] == "":
                item[date_type] = None
            else:
                date = tmp.str2date(item[date_type])
                if not date:
                    item["Error"] = f"{item[date_type]}が日付に変更できません"
                item[date_type] = date
        return item

    def button_delete(self):
        pass

    def button_up(self):
        self.change_order(-1.5)

    def button_down(self):
        self.change_order(+1.5)

    def change_order(self, c):
        indices = [idx for idx in self.w["table"].selection()]
        df = self.w["table"].df
        df.loc[indices, "Order"] += c
        self.update_table_contents(df)
        self.w["table"].selection_add(indices)

    def button_pull(self):
        df = self.SD[self.class_idx]
        df = df[df["Parent_ID"] == self.parent[0]]
        
        user_txt_list = []
        for idx in df.index:
            items = df.loc[idx, ["Name", "Total_Estimate_Hour", "Plan_Begin_Date", "Plan_End_Date"]].values
            user_txt_list.append(", ".join(map(str, items)))
        self.update_input_area(user_txt_list)