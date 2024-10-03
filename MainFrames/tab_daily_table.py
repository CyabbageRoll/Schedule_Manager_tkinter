from collections import defaultdict
import datetime
import tkinter as tk
import pandas as pd

import SubFrames as sf

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
        self.w = defaultdict(list)
        """label_combo : {label_text: [initial value, [combobox item list], state, label_width_ratio]} """
        label_combo = {}
        for k in self.SD.di.columns:
            label_combo[k] = [k, [], "normal", 12]
        self.w["Info_area"] = sf.InputListArea(self, label_combo_dict=label_combo)
        
        # 1日の予定入力欄
        self.w["table"] = sf.ScrollableTable(self, df=self.df, widths=[100, 250, 250])

    def pack_widgets(self):
        self.w["Info_area"].pack(side=tk.TOP, fill=tk.X, expand=False)
        self.w["table"].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def set_init(self):
        pass

            
