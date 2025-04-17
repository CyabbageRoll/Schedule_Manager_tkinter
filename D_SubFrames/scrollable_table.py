from collections import OrderedDict
import tkinter as tk
from tkinter import ttk


# import pandas as pd
class ScrollableTable(tk.Frame):
    def __init__(self, master,
                 df, show="headings", non_display_indices=[], widths=None, base_color="#bbbbbb", init_row=0,
                 **kwargs):
        super().__init__(master, **kwargs)
        # self.logger = master.logger
        # self.font = master.font
        self.df = df
        self.non_ids = non_display_indices
        self.base_color = base_color
        self.init_row = init_row
        self.set_variables()
        self.set_widgets(widths, show)
        self.pack_widgets()
        self.set_init()

    def set_variables(self):
        pass

    def set_widgets(self, widths, show):
        # 作成したwidgetsは辞書の中に保管する
        self.w = OrderedDict()
        
        # Treeview 列名はデータフレームのカラム名。行やデータの中身はまだ設定しない
        self.w["tree"] = ttk.Treeview(self, columns=self.df.columns.tolist(), show=show)
        widths = [200] * self.df.shape[1] if widths is None else widths
        for c, w in zip(self.df.columns, widths):
            self.w["tree"].column(c, stretch=tk.YES, anchor="center", width=w)
            self.w["tree"].heading(c, text=c)
        
        # Scroll barの設定
        self.w["scroll_h"] = ttk.Scrollbar(self, orient="horizontal", command=self.w["tree"].xview)
        self.w["scroll_v"] = ttk.Scrollbar(self, orient="vertical", command=self.w["tree"].yview)
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
            self.w["tree"].insert("", "end", iid=idx, values=self.df.loc[idx, :].tolist(), tag=idx)
            self.w["tree"].tag_configure(idx, background=self.base_color)
        if len(self.df.index) > self.init_row:
            self.w["tree"].see(self.df.index[self.init_row])

    # 一つのセルの値を更新する
    def update_cell(self, index, column, value):
        if index not in self.df.index:
            self.w["tree"].insert("", "end", iid=index, values=[None]*self.df.shape[1], tag=index)
        self.w["tree"].set(item=index, column=column, value=value)
        self.df.loc[index, column] = value

    # 一つの行の値を更新する
    def update_row(self, index, row_values):
        if index not in self.df.index:
            self.w["tree"].insert("", "end", iid=index, values=[None]*self.df.shape[1], tag=index)
        self.df.loc[index, :] = row_values
        self.w["tree"].item(item=index, values=row_values)

    # 内容を新しいデータフレームで更新
    def refresh(self, df, non_display_indices=[]):
        self.delete_current_items()
        self.df = df
        self.non_ids = non_display_indices
        self.set_init()

    def delete_current_items(self):
        del_ids = [idx for idx in self.df.index.tolist() if idx not in self.non_ids]
        self.w["tree"].delete(*del_ids)

    # 選択行の取得
    def selection(self):
        return self.w["tree"].selection()

    def selection_add(self, ids):
        self.w["tree"].selection_add(*ids)

    def set_cell_color(self, row, color):
        if color == "base":
            self.w["tree"].tag_configure(f"{row}", background=self.base_color)
        else:
            self.w["tree"].tag_configure(f"{row}", background=color)


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

    test_tk.mainloop()