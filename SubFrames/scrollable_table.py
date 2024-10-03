from collections import OrderedDict
import tkinter as tk
from tkinter import ttk

# import pandas as pd


class ScrollableTable(tk.Frame):
    def __init__(self, master, df, non_display_indices=[], widths=None, **kwargs):
        super().__init__(master, **kwargs)
        # self.logger = master.logger
        # self.font = master.font
        self.df = df
        self.non_ids = non_display_indices
        self.set_variables()
        self.set_widgets(widths)
        self.pack_widgets()
        self.set_init()

    def set_variables(self):
        pass

    def set_widgets(self, widths):
        # 作成したwidgetsは辞書の中に保管する
        self.w = OrderedDict()
        
        # Treeview 列名はデータフレームのカラム名。行やデータの中身はまだ設定しない
        self.w["tree"] = ttk.Treeview(self, columns=self.df.columns.tolist(), show="headings")
        widths = [200] * self.df.shape[1] if widths is None else widths
        for c, w in zip(self.df.columns, widths):
            self.w["tree"].column(c, stretch=tk.YES, anchor="center", width=w)
            self.w["tree"].heading(c, text=c)
        
        # Scroll barの設定
        self.w["scroll_h"] = ttk.Scrollbar(self, orient="horizontal", command=self.w["tree"].yview)
        self.w["scroll_v"] = ttk.Scrollbar(self, orient="vertical", command=self.w["tree"].xview)
        self.w["tree"]['xscrollcommand'] = self.w["scroll_h"].set
        self.w["tree"]['yscrollcommand'] = self.w["scroll_v"].set

    def pack_widgets(self):
        self.w["tree"].grid(row=0, column=0, sticky=tk.NSEW)
        self.w["scroll_h"].grid(row=1, column=0, sticky=tk.EW)
        self.w["scroll_v"].grid(row=0, column=1, sticky=tk.NS)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    def set_init(self):
        # データフレームの中身を設定する
        for idx in self.df.index:
            if idx in self.non_ids:
                continue
            self.w["tree"].insert("", "end", iid=idx, values=self.df.loc[idx, :].tolist())

    # 一つのセルの値を更新する
    def update_cell(self, index, column, value):
        self.w["tree"].set(item=index, column=column, value=value)
        self.df.loc[index, column] = value

    # 一つの行の値を更新する
    def update_row(self, index, row_values):
        self.df.loc[index, :] = row_values
        self.w["tree"].item(item=index, values=row_values)

    # 内容を新しいデータフレームで更新
    def refresh(self, df, non_display_indices=[]):
        del_ids = [idx for idx in self.df.index.tolist() if idx not in self.non_ids]
        self.w["tree"].delete(*del_ids)
        self.df = df
        self.non_ids = non_display_indices
        self.set_init()

    # 選択行の取得
    def selection(self):
        return self.w["tree"].selection()

    def selection_add(self, ids):
        self.w["tree"].selection_add(*ids)


if __name__ == "__main__":

    import pandas as pd

    class TestTk(tk.Tk):
        def __init__(self, df):
            super().__init__()
            self.geometry(f"400x400")
            self.frame = ScrollableTable(self, df, non_display_indices=["R03"])
            self.frame.pack(fill=tk.BOTH, expand=True)

    columns = [f"C{i:02d}" for i in range(10)]
    data = {f"R{j:02d}": [f"{j:02d}{i:02d}" for i in range(10)] for j in range(20)}
    df = pd.DataFrame.from_dict(data=data, orient="index", columns=columns)
    
    test_tk = TestTk(df)
    test_tk.frame.update_cell(index="R02", column="C03", value=100)
    test_tk.frame.update_row(index="R05", row_values=[i for i in range(10)])
    test_tk.frame.refresh(df.iloc[1:19, :], non_display_indices=["R07", "R09"])

    test_tk.frame.selection_add(["R02", "R03", "R04"])
    ids = test_tk.frame.selection()
    print(ids)

    test_tk.mainloop()