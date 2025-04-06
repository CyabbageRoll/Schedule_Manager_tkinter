# default
from collections import OrderedDict
import tkinter as tk
from tkinter import ttk
# additional
import pandas as pd
# user
import D_SubFrames as sf


class ProjectDisplay(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.edit_att_menu_click = None
        self.edit_ticket_menu_click = None
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["Refresh_button"] =  ttk.Button(self, text="Refresh", command=self.refresh_button_press, style="My.TButton")
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
        self.w["Table"].save_expanded_state()
        self.w["Table"].delete_current_items()
        self.w["Table"].set_init()
        self.w["Table"].restore_expanded_state()

    def set_bind(self):
        self.w["Table"].w["tree"].bind("<ButtonPress-2>", self.mouse_click_right)
        self.w["Table"].w["tree"].bind("<ButtonPress-3>", self.mouse_click_right)

    def mouse_click_right(self, event):
        idx = self.w["Table"].w["tree"].selection()
        if not idx:
            return

        tmp_idx = idx
        for i in range(5):
            parent_item = self.w["Table"].w["tree"].parent(tmp_idx)
            if parent_item == "":
                break
            tmp_idx = parent_item
        class_idx = i + 1
        self.show_menu(event, class_idx, idx[0])

    def show_menu(self, event, class_idx, idx):
        # メニューを指定した位置に表示
        popup_menu = tk.Menu(self, tearoff=0)
        popup_menu.add_command(label="編集", command=lambda : self.edit_ticket_menu_click(class_idx, idx))
        popup_menu.add_command(label="ATT", command=lambda : self.edit_att_menu_click(class_idx, idx))
        popup_menu.post(event.x_root, event.y_root)


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

    def save_expanded_state(self):
        # 再帰的に展開されているアイテムのIDを保存
        self.expanded_items = []
        self._save_expanded_state_recursive('')

    def _save_expanded_state_recursive(self, parent):
        for item in self.w["tree"].get_children(parent):
            if self.w["tree"].item(item, 'open'):
                self.expanded_items.append(item)
                # 子アイテムも再帰的にチェック
                self._save_expanded_state_recursive(item)

    def restore_expanded_state(self):
        for item in self.expanded_items:
            if self.w["tree"].exists(item):
                self.w["tree"].item(item, open=True)
