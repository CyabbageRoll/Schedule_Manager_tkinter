# default
from collections import OrderedDict
import tkinter as tk
# additional
import pandas as pd
# user
import SubFrames as sf


class ProjectDisplay(tk.Frame):
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
        self.w["Refresh_button"] =  tk.Button(self, text="Refresh", command=self.refresh_button_press, font=self.font, height=1)
        H = ["Owner", "Status", "Plan_Begin_Date", "Plan_End_Date", "Total_Estimate_Hour", "Actual_Hour"]
        I = {"1": [1]*len(H)}
        df = pd.DataFrame.from_dict(I, columns=H, orient="index")
        self.w["Table"] = ScrollableTableTree(self, df, show=["tree", "headings"])

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = True
            if k == "Refresh_button":
                e = False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def refresh_button_press(self):
        self.set_init()

    def set_init(self):
        self.w["Table"].delete_current_items()
        self.w["Table"].set_init()

    def set_bind(self):
        pass


class ScrollableTableTree(sf.ScrollableTable):
    def __init__(self, master, df, show, non_display_indices=[], widths=None, **kwargs):
        self.SD = master.SD
        super().__init__(master, df, show, non_display_indices, widths, **kwargs)

    def set_init(self):
        columns = self.df.columns.tolist()
        for i in range(5):
            for idx in self.SD[i+1].index:
                p_id = self.SD[i+1].loc[idx, "Parent_ID"]
                name = self.SD[i+1].loc[idx, "Name"]
                v = self.SD[i+1].loc[idx, columns].tolist()
                if p_id == "0":
                    p_id = ""
                self.w["tree"].insert(parent=p_id,
                                      index="end",
                                      iid=idx,
                                      text=name,
                                      values=v)

    def delete_current_items(self):
        for item in self.w["tree"].get_children():
            self.w["tree"].delete(item)