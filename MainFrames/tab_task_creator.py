from collections import OrderedDict
import tkinter as tk
from tkinter import messagebox
# user
import SubFrames as sf
import DataSettingRW as ds

class TaskCreator(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.prj_item = {i+1: "" for i in range(4)}
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()
        self.logger.debug("initialized Daily Table Tab")

    def set_variables(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()

        buttons = [["Create", self.press_create], 
                   ["Update", self.press_update],
                   ["Delete", self.press_delete]]
        self.w["buttons"] = sf.ButtonRow(self, buttons=buttons)
        self.w["text1"] = tk.Label(self, text="Task Information", font=self.font)

        # PROJECT1~4
        prj_items = {f"Project{i+1}": ["combobox", ["", [], "normal"]] for i in range(4)}
        self.w["prj"] = sf.InputListArea(self, input_rows=prj_items, label_width=20)

        # display task id
        task_items = OrderedDict()
        self.task_inputs = ["Task", "Status", "Total_Estimate_Hour", "Color"]
        self.task_date = ["Plan_Begin_Date", "Plan_End_Date"]
        self.task_info = ["Actual_Begin_Date", "Actual_End_Date", "Actual_Hour"]
        task_items["Task_ID"] = ["combobox", ["", [], "disabled"]]
        task_items["Task"] = ["combobox", ["", [], "normal"]]
        task_items["Status"] = ["combobox", ["", [], "normal"]]
        task_items["Total_Estimate_Hour"] = ["combobox", ["", [], "normal"]]
        task_items["Color"] = ["color", [""]]
        task_items["Plan_Begin_Date"] = ["date", ["", None]]
        task_items["Plan_End_Date"] = ["date", ["", None]]
        task_items["Actual_Begin_Date"] = ["combobox", ["", [], "disabled"]]
        task_items["Actual_End_Date"] = ["combobox", ["", [], "disabled"]]
        task_items["Actual_Hour"] = ["combobox", ["", [], "disabled"]]
        self.w["task"] = sf.InputListArea(self, input_rows=task_items, label_width=20)
        
        # PROJECT SUB CONTENTS INPUT
        self.w["Memo_label"] = tk.Label(self, text="Memo", font=self.font)
        self.w["Memo"] = tk.Text(self, font=self.font)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH if k == "Memo" else tk.X
            e = True if k == "Memo" else False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def set_init(self):
        self.w["task"].set_list("Status", ["TODO", "WIP", "DONE", "STORE", "CANCELED"])
        idx = self.SD[5].index[0]
        self.set_values_from_task_idx(idx)

    def set_values_from_task_idx(self, task_id):
        self.reset_task_items()
        self.logger.debug(f"show task info id = {task_id}")
        if task_id not in self.SD[5].index:
            self.error(f"task id {task_id} was not FOUND")
            return
        
        self.w["task"].set("Task_ID", task_id)
        prj_ids = self.find_prj_ids_from_task_id(task_id)
        for i, idx in enumerate(prj_ids):
            item = self.SD[i+1].loc[idx, f"Name"]
            self.w["prj"].set(f"Project{i+1}", item)
            self.prj_item[i+1] = item
        self.update_candidates(prj_ids)

        # Task information
        for ti in self.task_inputs:
            col = ti if ti != "Task" else "Name"
            self.w["task"].set(ti, self.SD[5].loc[task_id, col])
        for ti in self.task_date:
            self.w["task"].set(ti, self.SD[5].loc[task_id, ti])
        for ti in self.task_info:
            self.w["task"].set(ti, self.SD[5].loc[task_id, ti])
        # Memo
        self.w["Memo"].insert(0.0, self.SD[5].loc[task_id, "Memo"])

    def reset_task_items(self):
        for ti in self.task_inputs:
            if ti != "Task":
                self.w["task"].set(ti, "")
        for ti in self.task_date:
            self.w["task"].set(ti, "")
        for ti in self.task_info:
            self.w["task"].set(ti, "")
        self.w["Memo"].delete(0., tk.END)

    def find_prj_ids_from_task_id(self, task_id):
        # task_id　から　[prj1_idx, prj2_idx, prj3_idx, prj4_idx]を返す関数
        idx = task_id
        prj_ids = []
        for i in range(4):
            idx = self.SD[5-i].loc[idx, "Parent_ID"]
            prj_ids.append(idx)
        return prj_ids[::-1]
    
    def find_prj_ids_from_input(self):
        ids = []
        idx = "0"
        for i in range(1, 5):
            prj = self.w["prj"].get(f"Project{i}")
            idx = self.specify_prj_idx(self.SD[i], prj, idx)
            ids.append(idx)
        return ids

    def update_candidates(self, prj_ids):
        # Projectの候補を調べてドロップダウンリストにセットする
        for i, idx in enumerate(["0"] + prj_ids):
            candidate_list = self.SD[i+1][self.SD[i+1]["Parent_ID"] == idx]["Name"].tolist()
            if candidate_list:
                if i < 4:
                    self.w["prj"].set_list(f"Project{i+1}", candidate_list)
                if i == 4:
                    self.w["task"].set_list("Task", candidate_list)
            else:
                break

    def task_item_from_current_inputs(self):
        ids = self.find_prj_ids_from_input()
        task = [self.w["task"].get("Task"),
                ids[3],
                "Administrator",
                self.w["task"].get("Status"),
                self.w["task"].get("Plan_Begin_Date"),
                self.w["task"].get("Plan_End_Date"),
                self.w["task"].get("Total_Estimate_Hour"),
                self.w["task"].get("Actual_Begin_Date"),
                self.w["task"].get("Actual_End_Date"),
                self.w["task"].get("Actual_Hour"),
                self.w["task"].get_as_hex("Color"),
                self.w["Memo"].get("1.0", "end"),
                "c1", "c2", "c3", "c4", "c5"
        ]

        return task

    def new_projects(self):
        # project名とそれが新しいアイテムか否かを返す
        new_prj = [(self.w["prj"].get(f"Project{i+1}"), True) for i in range(4)]
        # Projectが新規か否かをチェック
        idx = "0"  # prj1の親IDは"0"
        for i, (prj, _) in enumerate(new_prj):
            df = self.SD[i+1]
            df = df[df["Parent_ID"] == idx]
            if prj in df["Name"].tolist():
                idx = df.index[df["Name"] == prj][0]
                new_prj[i] = (prj, False)
            else:
                break
        return new_prj

    def specify_prj_idx(self, df, prj, p_id):
        # prj名と親IDから自分のidxを特定する
        df = df[df.iloc[:, 1] == p_id]
        idx = df.index[df.iloc[:, 0] == prj]
        idx = idx[0] if len(idx) else None
        return idx

    def create_projects(self, new_prj):
        # prj1から順番に登録していく
        idx = "0"
        for i, (prj, flag) in enumerate(new_prj):
            if flag:
                ret = messagebox.askokcancel(title="System", message=f"Project{i+1}: {prj}はありません。新規に作成しますか？")
                if ret:
                    new_items = [prj, idx]
                    ds.add_list_to_df_last_row(self.SD[i+1], new_items)
                    self.logger.info(f"add new prj{i+1} item : {idx=} : {prj=}")
                else:
                    return False
            idx = self.specify_prj_idx(self.SD[i+1], prj, idx)
        return True
    
    def press_create(self):
        # 親projectの存在を確認して、ない場合は作成する
        new_prj = self.new_projects()
        self.logger.debug(f"task create button was pressed {new_prj=}")
        ret = self.create_projects(new_prj)
        # projectの作成を途中で辞めた場合はtask作成を中止する
        if not ret:
            return
        task_item = self.task_item_from_current_inputs()
        self.logger.debug(f"Create task : {task_item=}")
        if not ds.add_list_to_df_last_row(self.SD[5], task_item, exist_ok=False):
            messagebox.showerror(title="System", message=f"そのtaskはすでに存在します")

    def press_update(self):
        new_prj = self.new_projects()
        for i, (prj, flag) in enumerate(new_prj):
            if flag:
                messagebox.showinfo(title="System", message=f"Project{i+1} : {prj}が存在しません。新規で作成する場合はCreateボタンを押してください")
                return
        task_item = self.task_item_from_current_inputs()
        task_id = self.w["task"].get("Task_ID")
        self.logger.debug(f"Update task : {task_id=}, {task_item=}")
        ds.add_list_to_df_last_row(self.SD[5], task_item, exist_ok=True, idx=task_id)

    def press_delete(self):
        pass

    def set_bind(self):
        self.w["prj"].w["Project1"].bind("<FocusOut>", lambda x: self.prj_box_focus_out(x, 1))
        self.w["prj"].w["Project2"].bind("<FocusOut>", lambda x: self.prj_box_focus_out(x, 2))
        self.w["prj"].w["Project3"].bind("<FocusOut>", lambda x: self.prj_box_focus_out(x, 3))
        self.w["prj"].w["Project4"].bind("<FocusOut>", lambda x: self.prj_box_focus_out(x, 4))
        self.w["task"].w["Task"].bind("<FocusOut>", self.task_box_focus_out)
        self.w["task"].w["Total_Estimate_Hour"].bind("<FocusOut>",
                                                lambda x: self.float_box_focus_out(x, "Total_Estimate_Hour"))

    def prj_box_focus_out(self, event, prj_no):
        # 自分より下の子を空白にする
        item = self.w["prj"].get(f"Project{prj_no}")
        if item == self.prj_item[prj_no]:
            return
        else:
            self.prj_item[prj_no] = item
            for i in range(prj_no+1, 5):
                self.w["prj"].set(f"Project{i}", "")
                self.w["prj"].set_list(f"Project{i}", [])
            self.w["task"].set(f"Task", "")
            self.w["task"].set_list(f"Task", [])
            self.w["task"].set(f"Task_ID", "")

        # ドロップダウンリストを更新
        prj_ids = self.find_prj_ids_from_input()
        self.update_candidates(prj_ids)

    def task_box_focus_out(self, event):
        # タスク名が空なら飛ばす
        task = self.w["task"].get("Task")
        if not task:
            self.reset_task_items()
            return
        # projectが存在しないなら飛ばす
        ids = self.find_prj_ids_from_input()
        prj_id = ids[3]
        if prj_id is None:
            self.reset_task_items()
            return
        # task idを調べる
        idx = self.specify_prj_idx(self.SD[5], task, prj_id)
        if idx:
            self.w["task"].set("Task_ID", idx)
            self.set_values_from_task_idx(idx)
        else:
            self.w["task"].set("Task_ID", "")
            self.reset_task_items()

    def float_box_focus_out(self, event, box_name):
        pass
