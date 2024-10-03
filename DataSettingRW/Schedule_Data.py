import os
from dataclasses import dataclass, asdict, field
from typing import List
import hashlib

import pandas as pd


@dataclass
class ScheduleData:
    prj1: pd.DataFrame = ""
    prj2: pd.DataFrame = ""
    prj3: pd.DataFrame = ""
    prj4: pd.DataFrame = ""
    task: pd.DataFrame = ""
    todo: pd.DataFrame = ""
    dt : pd.DataFrame = ""
    di : pd.DataFrame = ""


def read_schedule_data(db_dir):
    SD = ScheduleData()
    SD.prj1, SD.prj2, SD.prj3, SD.prj4, SD.task, SD.todo, SD.dt, SD.di = read_df_pkl(db_dir)
    return SD


def read_df_pkl(db_dir):
    prj1 = pd.read_pickle(os.path.join(db_dir, "prj1_df.pkl"))
    prj2 = pd.read_pickle(os.path.join(db_dir, "prj2_df.pkl"))
    prj3 = pd.read_pickle(os.path.join(db_dir, "prj3_df.pkl"))
    prj4 = pd.read_pickle(os.path.join(db_dir, "prj4_df.pkl"))
    task = pd.read_pickle(os.path.join(db_dir, "task_df.pkl"))
    todo = pd.read_pickle(os.path.join(db_dir, "todo_df.pkl"))
    dt = pd.read_pickle(os.path.join(db_dir, "daily_table_df.pkl"))
    di = pd.read_pickle(os.path.join(db_dir, "daily_info_df.pkl"))
    return prj1, prj2, prj3, prj4, task, todo, dt, di


def save_df_as_pkl(SD, db_dir):
    SD.prj1.to_pickle(os.path.join(db_dir, "prj1_df.pkl"))
    SD.prj2.to_pickle(os.path.join(db_dir, "prj2_df.pkl"))
    SD.prj3.to_pickle(os.path.join(db_dir, "prj3_df.pkl"))
    SD.prj4.to_pickle(os.path.join(db_dir, "prj4_df.pkl"))
    SD.task.to_pickle(os.path.join(db_dir, "task_df.pkl"))
    SD.todo.to_pickle(os.path.join(db_dir, "todo_df.pkl"))
    SD.dt.to_pickle(os.path.join(db_dir, "daily_table_df.pkl"))
    SD.di.to_pickle(os.path.join(db_dir, "daily_info_df.pkl"))


def list_to_hash(input_list):
    str_list = [f"{si}" for si in input_list]
    s = "-".join(str_list)
    return hashlib.md5(s.encode()).hexdigest()[:10]


def add_list_to_df_last_row(df, new_items, exist_ok=False):
    idx = list_to_hash(new_items[:2])
    flag = True
    if idx not in df.index.tolist():
        df.loc[idx, :] = new_items
    elif exist_ok:
        df.loc[idx, :] = new_items
    else:
        flag = False
    return flag

if __name__ == "__main__":

    db_dir = r"../DB_DIR"
    SD = ScheduleData()
    SD = read_schedule_data(db_dir)
    print(SD)

    CREATE_SAMPLE = False
    CREATE_SAMPLE = True
    if CREATE_SAMPLE:

        # Project & Task
        LABEL_COMMON =["Status", 
                       "Plan_Begin_Date", "Plan_End_Date", "Total_Estimate_Hour",
                       "Actual_Begin_Date", "Actual_End_Date", "Actual_Hour",
                       "Color", "Memo", "Col1", "Col2", "Col3", "Col4", "Col5"]
        LABEL_PRJ1 = ["Prj1", "Prj0_ID"]
        LABEL_PRJ2 = ["Prj2", "Prj1_ID"]
        LABEL_PRJ3 = ["Prj3", "Prj2_ID"]
        LABEL_PRJ4 = ["Prj4", "Prj3_ID"]
        LABEL_TASK = ["Task", "Prj4_ID"] + LABEL_COMMON
        LABEL_TODO = ["TODO", "Task_ID"] + ["InCharge", "Order"] + LABEL_COMMON

        prj1 = []
        prj1.append(["P1_1", "0"])
        prj1.append(["P1_2", "0"])
        prj1 = {list_to_hash(c[0:2]): c for c in prj1}
        prj1_ids = list(prj1.keys())

        prj2 = []
        prj2.append(["P2_1", prj1_ids[0]])
        prj2.append(["P2_2", prj1_ids[0]])
        prj2.append(["P2_1", prj1_ids[1]])
        prj2.append(["P2_2", prj1_ids[1]])
        prj2 = {list_to_hash(c[0:2]): c for c in prj2}
        prj2_ids = list(prj2.keys())

        prj3 = []
        prj3.append(["P3_1", prj2_ids[1]])
        prj3.append(["P3_2", prj2_ids[1]])
        prj3.append(["P3_3", prj2_ids[1]])
        prj3.append(["P3_2", prj2_ids[0]])
        prj3.append(["P3_1", prj2_ids[2]])
        prj3 = {list_to_hash(c[0:2]): c for c in prj3}
        prj3_ids = list(prj3.keys())

        prj4 = []
        prj4.append(["Lunch", prj3_ids[1]])
        prj4.append(["Dinner", prj3_ids[1]])
        prj4.append(["Breakfast", prj3_ids[1]])
        prj4.append(["P4_2", prj3_ids[0]])
        prj4.append(["P4_1", prj3_ids[2]])
        prj4 = {list_to_hash(c[0:2]): c for c in prj4}
        prj4_ids = list(prj4.keys())

        task = []
        task.append(["Fried Egg", prj4_ids[2], "TODO", 20250301, 20250301, 10, 0, 0, 0, "#aaaaaa", "memo1", "c1", "c2", "c3", "c4", "c5"])
        task.append(["Rice", prj4_ids[2], "TODO", 20250301, 20250301, 20, 0, 0, 0, "#aaaaaa", "memo1", "c1", "c2", "c3", "c4", "c5"])
        task.append(["Ramen", prj4_ids[0], "TODO", 20250101, 20250301, 30, 0, 0, 0, "#aaaaaa", "memo1", "c1", "c2", "c3", "c4", "c5"])
        task.append(["Salad", prj4_ids[1], "TODO", 20250301, 20250301, 40, 0, 0, 0, "#aaaaaa", "memo1", "c1", "c2", "c3", "c4", "c5"])
        task.append(["Hamburger", prj4_ids[1], "TODO", 20250301, 20250301, 50, 0, 0, 0, "#aaaaaa", "memo1", "c1", "c2", "c3", "c4", "c5"])
        task.append(["Fried Potato", prj4_ids[1], "TODO", 20250201, 20250301, 60, 0, 0, 0, "#aaaaaa", "memo1", "c1", "c2", "c3", "c4", "c5"])
        task = {list_to_hash(t[0:2]): t for t in task}
        task_ids = list(task.keys())

        todo = []
        todo.append(["Fry eggs", task_ids[0], "user", 1, "TODO", 0, 0, 3, 0, 0, 0, "#bbbbbb", "memo", "c1", "c2", "c3", "c4", "c5"])
        todo.append(["eat eggs", task_ids[0], "user", 2, "TODO", 0, 0, 3, 0, 0, 0, "#bbbbbb", "memo", "c1", "c2", "c3", "c4", "c5"])
        todo.append(["microwave", task_ids[1], "user", 1, "TODO", 0, 0, 3, 0, 0, 0, "#bbbbbb", "memo", "c1", "c2", "c3", "c4", "c5"])
        todo.append(["Chopped Onion", task_ids[4], "user", 1, "TODO", 0, 0, 3, 0, 0, 0, "#bbbbbb", "memo", "c1", "c2", "c3", "c4", "c5"])
        todo.append(["Knead", task_ids[4], "user", 2, "TODO", 0, 0, 3, 0, 0, 0, "#bbbbbb", "memo", "c1", "c2", "c3", "c4", "c5"])
        todo.append(["Bake", task_ids[4], "user", 3, "TODO", 0, 0, 3, 0, 0, 0, "#bbbbbb", "memo", "c1", "c2", "c3", "c4", "c5"])
        todo = {list_to_hash(t[0:2]): t for t in todo}
        todo_ids = list(task.keys())

        SD = ScheduleData()
        SD.prj1 = pd.DataFrame.from_dict(prj1, orient="index", columns=LABEL_PRJ1)
        SD.prj2 = pd.DataFrame.from_dict(prj2, orient="index", columns=LABEL_PRJ2)
        SD.prj3 = pd.DataFrame.from_dict(prj3, orient="index", columns=LABEL_PRJ3)
        SD.prj4 = pd.DataFrame.from_dict(prj4, orient="index", columns=LABEL_PRJ4)
        SD.task = pd.DataFrame.from_dict(task, orient="index", columns=LABEL_TASK)
        SD.todo = pd.DataFrame.from_dict(todo, orient="index", columns=LABEL_TODO)

        print(SD.prj1)
        print(SD.prj2)
        print(SD.prj3)
        print(SD.prj4)
        print(SD.task)
        print(SD.todo)

        STATUS = ["TODO", "WIP", "DONE", "STORE", "CANCELED"]

        # Track Table
        DAILY_TABLE = [f"{i//4:02d}{(i%4)*15:02d}" for i in range(24*4)] + \
                      ["TOTAL", "FROM", "TO", "BREAK"]
        DAILY_ITEMS = ["Health", "Work_Place", "Safety", "OverWork", "Info1", "Info2", "Info3"]
        SD.dt = pd.DataFrame(columns=DAILY_TABLE)
        SD.di = pd.DataFrame(columns=DAILY_ITEMS)

        print(SD.dt)
        print(SD.di)
 
        save_df_as_pkl(SD, db_dir)