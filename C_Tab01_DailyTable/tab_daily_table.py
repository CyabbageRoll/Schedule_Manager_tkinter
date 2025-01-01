from collections import OrderedDict
import datetime
import tkinter as tk
import pandas as pd

import D_SubFrames as sf

class DailyInformation(tk.Frame):
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
        for k in self.SD["daily_info"].columns:
            input_rows[k] = ["combobox", [k, [], "normal"]]
        self.w["Info_area"] = sf.InputListArea(self, input_rows=input_rows, label_width=12)
        
        # 1日の予定入力欄
        self.w["table"] = sf.ScrollableTable(self, df=self.df, widths=[100, 250, 250])

    def pack_widgets(self):
        self.w["Info_area"].pack(side=tk.TOP, fill=tk.X, expand=False)
        self.w["table"].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def set_init(self):
        pass

            
