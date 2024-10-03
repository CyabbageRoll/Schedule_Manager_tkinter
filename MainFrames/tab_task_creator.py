from collections import defaultdict
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
        self.prj = {1: self.SD.prj1, 2: self.SD.prj2, 3: self.SD.prj3, 4: self.SD.prj4, 5: self.SD.task}
        self.prj_item = {i+1: "" for i in range(4)}
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()
        self.logger.debug("initialized Daily Table Tab")

    def set_variables(self):
        self.memo = tk.StringVar()

    def set_widgets(self):
        self.w = defaultdict(list)

        buttons = [["Create", self.press_create], 
                   ["Update", self.press_update],
                   ["Delete", self.press_delete]]
        self.w["buttons"] = sf.ButtonRow(self, buttons=buttons)
        self.w["text1"] = tk.Label(self, text="Task Information", font=self.font)
        
        # PROJECT1~4
        code_list = {f"Project{i+1}": ["", [], "normal", 20] for i in range(4)}
        self.w["prj_inputs"] = sf.InputListArea(self, label_combo_dict=code_list)
        
        # display task id
        self.w["task_idx"] = sf.InputListArea(self, {"Task_ID": ["", [], "disabled", 20]})

        # PROJECT CONTENTS INPUT
        self.task_inputs = ["Task", "Status", "Plan_Begin_Date", "Plan_End_Date", "Total_Estimate_Hour", "Color"]
        code_list = {ti: ["", [], "normal", 20] for ti in self.task_inputs}
        self.w["task_inputs"] = sf.InputListArea(self, label_combo_dict=code_list)
        
        # PROJECT CONTENTS READ ONLY
        t = ["Actual_Begin_Date", "Actual_End_Date", "Actual_Hour"]
        code_list = {ti: ["", [], "disabled", 20] for ti in t}
        self.w["task_info"] = sf.InputListArea(self, label_combo_dict=code_list)
        
        # PROJECT SUB CONTENTS INPUT
        self.w["Memo_label"] = tk.Label(self, text="Memo", font=self.font)
        self.w["Memo"] = tk.Text(self)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH if k == "Memo" else tk.X
            e = True if k == "Memo" else False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def set_init(self):
        self.w["task_inputs"].set_list("Status", ["TODO", "WIP", "DONE", "STORE", "CANCELED"])
        idx = self.SD.task.index[0]
        self.set_as_project_idx(idx)

    def set_as_project_idx(self, task_id):
        if task_id not in self.SD.task.index:
            self.error(f"task id {task_id} was not FOUND")
            return
        
        self.w["task_idx"].set("Task_ID", task_id)
        prj_ids = self.find_prj_ids_from_task_id(task_id)
        for i, idx in enumerate(prj_ids):
            item = self.prj[i+1].loc[idx, f"Prj{i+1}"]
            self.w["prj_inputs"].set(f"Project{i+1}", item)
            self.prj_item[i+1] = item
        self.update_candidates(*prj_ids)

        # Task information
        for ti in self.task_inputs:
            self.w["task_inputs"].set(ti, self.SD.task.loc[task_id, ti])
        # Memo
        self.memo.set(self.SD.task.loc[task_id, "Memo"])

    def find_prj_ids_from_task_id(self, task_id):
        prj4_idx = self.SD.task.loc[task_id, "Prj4_ID"]
        prj3_idx = self.SD.prj4.loc[prj4_idx, "Prj3_ID"]
        prj2_idx = self.SD.prj3.loc[prj3_idx, "Prj2_ID"]
        prj1_idx = self.SD.prj2.loc[prj2_idx, "Prj1_ID"]
        return prj1_idx, prj2_idx, prj3_idx, prj4_idx
    
    def find_prj_ids_from_input(self):
        ids = []
        idx = "0"
        for i in range(1, 5):
            prj = self.w["prj_inputs"].get(f"Project{i}")
            idx = self.specify_prj_idx(self.prj[i], prj, idx)
            ids.append(idx)
        return ids

    def update_candidates(self, prj1_idx, prj2_idx, prj3_idx, prj4_idx):
        # Projects Candidate
        prj1_lists = self.SD.prj1["Prj1"].tolist()
        prj2_lists = self.SD.prj2[self.SD.prj2["Prj1_ID"] == prj1_idx]["Prj2"].tolist()
        prj3_lists = self.SD.prj3[self.SD.prj3["Prj2_ID"] == prj2_idx]["Prj3"].tolist()
        prj4_lists = self.SD.prj4[self.SD.prj4["Prj3_ID"] == prj3_idx]["Prj4"].tolist()
        task_lists = self.SD.task[self.SD.task["Prj4_ID"] == prj4_idx]["Task"].tolist()
        self.w["prj_inputs"].set_list("Project1", prj1_lists)
        self.w["prj_inputs"].set_list("Project2", prj2_lists)
        self.w["prj_inputs"].set_list("Project3", prj3_lists)
        self.w["prj_inputs"].set_list("Project4", prj4_lists)
        self.w["task_inputs"].set_list("Task", task_lists)

    def task_item_from_current_inputs(self):
        ids = self.find_prj_ids_from_input()
        task = [self.w["task_inputs"].get("Task"),
                ids[3],
                self.w["task_inputs"].get("Status"),
                self.w["task_inputs"].get("Plan_Begin_Date"),
                self.w["task_inputs"].get("Plan_End_Date"),
                self.w["task_inputs"].get("Total_Estimate_Hour"),
                0, 0, 0,
                self.w["task_inputs"].get("Color"),
                self.memo.get(),
                "c1", "c2", "c3", "c4", "c5"
        ]
        return task

    def new_projects(self):
        # project名の取得
        new_prj = [(self.w["prj_inputs"].get(f"Project{i+1}"), True) for i in range(4)]
        # Projectが新規か否かをチェック
        idx = "0"  # prj1の親IDは"0"
        for i, (prj, _) in enumerate(new_prj):
            df = getattr(self.SD, f"prj{i+1}")
            df = df[df[f"Prj{i}_ID"] == idx]
            if prj in df[f"Prj{i+1}"].tolist():
                idx = df.index[df[f"Prj{i+1}"] == prj][0]
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
                ret = messagebox.askokcancel(title="System", message=f"prj{i+1}: {prj}はありません。新規に作成しますか？")
                if ret:
                    new_items = [prj, idx]
                    ds.add_list_to_df_last_row(self.prj[i+1], new_items)
                    self.logger.info(f"add new prj{i+1} item : {idx=} : {prj=}")
                else:
                    return False
            idx = self.specify_prj_idx(self.prj[i+1], prj, idx)
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
        if not ds.add_list_to_df_last_row(self.SD.task, task_item, exist_ok=False):
            messagebox.showerror(title="System", message=f"そのtaskはすでに存在します")
        # TODO : 型チェック等々が必要

    def press_update(self):
        new_prj = self.new_projects()
        for i, (prj, flag) in enumerate(new_prj):
            if flag:
                messagebox.showinfo(title="System", message=f"prj{i+1} : {prj}が存在しません。新規で作成する場合はCreateボタンを押してください")
                return
        task_item = self.task_item_from_current_inputs()
        self.logger.debug(f"Update task : {task_item=}")
        ds.add_list_to_df_last_row(self.SD.task, task_item, exist_ok=True)

    def press_delete(self):
        pass

    def set_bind(self):
            self.w["prj_inputs"].w["Project1"].bind("<FocusOut>", lambda x: self.prj_box_focus_out(x, 1))
            self.w["prj_inputs"].w["Project2"].bind("<FocusOut>", lambda x: self.prj_box_focus_out(x, 2))
            self.w["prj_inputs"].w["Project3"].bind("<FocusOut>", lambda x: self.prj_box_focus_out(x, 3))
            self.w["prj_inputs"].w["Project4"].bind("<FocusOut>", lambda x: self.prj_box_focus_out(x, 4))
            self.w["task_inputs"].w["Task"].bind("<FocusOut>", self.task_box_focus_out)
            self.w["task_inputs"].w["Plan_Begin_Date"].bind("<FocusOut>", 
                                                           lambda x: self.date_box_focus_out(x, "Plan_Begin_Date"))
            self.w["task_inputs"].w["Plan_End_Date"].bind("<FocusOut>",
                                                         lambda x: self.date_box_focus_out(x, "Plan_End_Date"))
            self.w["task_inputs"].w["Total_Estimate_Hour"].bind("<FocusOut>",
                                                               lambda x: self.int_box_focus_out(x, "Total_Estimate_Hour"))
            self.w["task_inputs"].w["Color"].bind("<FocusOut>", self.color_box_focus_out)

    def prj_box_focus_out(self, event, prj_no):
        # 自分より下の子を空白にする
        item = self.w["prj_inputs"].get(f"Project{prj_no}")
        print(item, self.prj_item[prj_no])
        if item == self.prj_item[prj_no]:
            return
        else:
            self.prj_item[prj_no] = item
            for i in range(prj_no+1, 5):
                self.w["prj_inputs"].set(f"Project{i}", "")
                self.w["prj_inputs"].set_list(f"Project{i}", [])
            self.w["task_inputs"].set(f"Task", "")
            self.w["task_inputs"].set_list(f"Task", [])
            self.w["task_idx"].set(f"Task_ID", "")
        # 自分の一つしたのリストを更新
        ids = self.find_prj_ids_from_input()
        print(ids)
        idx = ids[prj_no-1]
        if idx:
            if prj_no < 4:
                prj_lists = self.prj[prj_no+1][self.prj[prj_no+1][f"Prj{prj_no}_ID"] == idx][f"Prj{prj_no+1}"].tolist()
                self.w["prj_inputs"].set_list(f"Project{prj_no+1}", prj_lists)
            else:
                task_lists = self.SD.task[self.SD.task[f"Prj4_ID"] == idx][f"Task"].tolist()
                self.w["task_inputs"].set_list(f"Task", task_lists)

    def task_box_focus_out(self, event):
        # タスク名がからなら飛ばす
        task = self.w["task_inputs"].get("Task")
        if not task:
            return
        # projectが存在しないなら飛ばす
        ids = self.find_prj_ids_from_input()
        prj_id = ids[3]
        if prj_id is None:
            return
        # task idを調べる
        idx = self.specify_prj_idx(self.SD.task, task, prj_id)
        if idx:
            self.w["task_idx"].set("Task_ID", idx)
        else:
            self.w["task_idx"].set("Task_ID", "")

    def date_box_focus_out(self, event, box_name):
        pass

    def int_box_focus_out(self, event, box_name):
        pass

    def color_box_focus_out(self, event):
        pass