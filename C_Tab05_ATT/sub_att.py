# default
from collections import OrderedDict
import tkinter as tk
import datetime
# additional
import pandas as pd
# user
from A_DataSettingRW import type_converter, serial_numbering
import D_SubFrames as sf

class ATT(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.GP = master.GP
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
        self.msg.set(f"{parent=}, {selected_class=}, {idx=}")
        class_idx = self.w["selector"].class2idx[selected_class]
        df = self.SD[class_idx+1]
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
        pass

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
                print(self.df.max(axis=0)["Order"])
                item["Order"] += int(self.w["table"].df.max(axis=0)["Order"])
                for header in self.df.columns:
                    self.w["table"].update_cell(index, header, item[header])
            else:
                msg.append(inp + f" : {item['Error']}")
        msg.append("")
        self.update_input_area(user_txt_list=msg)

    def parse_string(self, s):
        s = s.split(",")
        if len(s) < 4:
            return None
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
            item["Error"] = f"{item['Name']}はすでに存在します"
            return item

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