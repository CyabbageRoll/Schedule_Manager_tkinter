import os
from dataclasses import dataclass, asdict, field
from typing import List
import hashlib
import datetime
import pandas as pd


def read_schedule_data(db_dir):
    prj1 = pd.read_pickle(os.path.join(db_dir, "prj1_df.pkl"))
    prj2 = pd.read_pickle(os.path.join(db_dir, "prj2_df.pkl"))
    prj3 = pd.read_pickle(os.path.join(db_dir, "prj3_df.pkl"))
    prj4 = pd.read_pickle(os.path.join(db_dir, "prj4_df.pkl"))
    task = pd.read_pickle(os.path.join(db_dir, "task_df.pkl"))
    todo = pd.read_pickle(os.path.join(db_dir, "todo_df.pkl"))
    daily_sch = pd.read_pickle(os.path.join(db_dir, "daily_table_df.pkl"))
    daily_info = pd.read_pickle(os.path.join(db_dir, "daily_info_df.pkl"))
    SD = {1: prj1, 2: prj2, 3: prj3, 4:prj4, 5: task, 6: todo, "daily_sch": daily_sch, "daily_info":daily_info}
    return SD


def save_schedule_data(SD, db_dir):
    SD[1].to_pickle(os.path.join(db_dir, "prj1_df.pkl"))
    SD[2].to_pickle(os.path.join(db_dir, "prj2_df.pkl"))
    SD[3].to_pickle(os.path.join(db_dir, "prj3_df.pkl"))
    SD[4].to_pickle(os.path.join(db_dir, "prj4_df.pkl"))
    SD[5].to_pickle(os.path.join(db_dir, "task_df.pkl"))
    SD[6].to_pickle(os.path.join(db_dir, "todo_df.pkl"))
    SD["daily_sch"].to_pickle(os.path.join(db_dir, "daily_table_df.pkl"))
    SD["daily_info"].to_pickle(os.path.join(db_dir, "daily_info_df.pkl"))


def list_to_hash_w_ms(input_list):
    str_list = [f"{si}" for si in input_list] + [datetime.datetime.now().strftime("%f")]
    s = "-".join(str_list)
    return hashlib.md5(s.encode()).hexdigest()[:10]


def numbering_item(input_list):
    str_list = [f"{si}" for si in input_list]
    s = "-".join(str_list)
    md5 = hashlib.md5(s.encode()).hexdigest()[:5]
    dd = datetime.datetime.now().strftime("%y%m%d")
    return md5 + dd


def add_list_to_df_last_row(df, new_items, exist_ok=False, idx=None):
    if not idx:
        idx = list_to_hash_w_ms(new_items[:3])
    
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
    # SD = read_schedule_data(db_dir)
    # for k, df in SD.items():
    #     print(k)
    #     print(df)

    CREATE_SAMPLE = False
    CREATE_SAMPLE = True
    if CREATE_SAMPLE:

        # Project & Task
        HEADERS = ["Name", "Parent_ID", "Owner", "Status", "Order", "Request",
                   "Plan_Begin_Date", "Plan_End_Date", "Total_Estimate_Hour",
                   "Actual_Begin_Date", "Actual_End_Date", "Actual_Hour",
                   "Color", "Goal", "Difficulty", "Memo", 
                   "Num_Active_Children", "Last_Update"]
                   

        TYPES = [str, str, str, str, int, str,
                 datetime.date, datetime.date, float,
                 datetime.date, datetime.date, float,
                 str, str, str, str,
                 int, datetime.date]

        INITIAL = [None, None, "Administrator", "TODO", 0, "Yes",
                   None, None, 0,
                   None, None, 0,
                   "Cyan", "Please Input", "", "",
                   0, datetime.date.today()]

        print(f"{len(HEADERS)=}")
        print(f"{len(TYPES)=}")
        print(f"{len(INITIAL)=}")

        prj1 = []
        prj1.append(["Prj1_1", "0"] + INITIAL[2:])
        prj1.append(["Prj1_2", "0"] + INITIAL[2:])
        prj1 = {numbering_item(c[0:3]): c for c in prj1}
        prj1_ids = list(prj1.keys())

        prj2 = []
        prj2.append(["P2_1", prj1_ids[0]] + INITIAL[2:])
        prj2.append(["P2_2", prj1_ids[0]] + INITIAL[2:])
        prj2.append(["P2_1", prj1_ids[1]] + INITIAL[2:])
        prj2.append(["P2_2", prj1_ids[1]] + INITIAL[2:])
        prj2 = {list_to_hash_w_ms(c[0:3]): c for c in prj2}
        prj2_ids = list(prj2.keys())

        prj3 = []
        prj3.append(["P3_1", prj2_ids[1]]  + INITIAL[2:])
        prj3.append(["P3_2", prj2_ids[1]]  + INITIAL[2:])
        prj3.append(["P3_3", prj2_ids[1]]  + INITIAL[2:])
        prj3.append(["P3_2", prj2_ids[0]]  + INITIAL[2:])
        prj3.append(["P3_1", prj2_ids[2]]  + INITIAL[2:])
        prj3 = {list_to_hash_w_ms(c[0:3]): c for c in prj3}
        prj3_ids = list(prj3.keys())

        prj4 = []
        prj4.append(["Lunch", prj3_ids[1]] + INITIAL[2:])
        prj4.append(["Dinner", prj3_ids[1]] + INITIAL[2:])
        prj4.append(["Breakfast", prj3_ids[1]] + INITIAL[2:])
        prj4.append(["P4_2", prj3_ids[0]] + INITIAL[2:])
        prj4.append(["P4_1", prj3_ids[2]] + INITIAL[2:])
        prj4 = {list_to_hash_w_ms(c[0:3]): c for c in prj4}
        prj4_ids = list(prj4.keys())

        task = []
        task.append(["Fried Egg", prj4_ids[2], "Administrator", "TODO", 0, "Yes", datetime.date(2025, 3, 10), datetime.date(2025, 3, 31), 10, None, None, 0, "Cyan", "Goal", "", "memo1", 0, datetime.date.today()])
        task.append(["Rice", prj4_ids[2], "Administrator", "TODO", 1, "Yes", datetime.date(2025, 4, 1), datetime.date(2025, 5, 5), 20, None, None, 0, "Cyan", "Goal", "", "memo1", 0, datetime.date.today()])
        task.append(["Ramen", prj4_ids[0], "Administrator", "TODO", 0, "Yes", datetime.date(2025, 5, 1), datetime.date(2025, 7, 20), 30, None, None, 0, "Cyan", "Goal", "", "memo1", 0, datetime.date.today()])
        task.append(["Salad", prj4_ids[1], "Administrator", "TODO", 0, "Yes", datetime.date(2025, 6, 1), datetime.date(2025, 8, 15), 40, None, None, 0, "Cyan", "Goal", "", "memo1", 0, datetime.date.today()])
        task.append(["Hamburger", prj4_ids[1], "Administrator", "TODO", 1, "Yes", datetime.date(2025, 7, 1), datetime.date(2025, 9, 30), 50, None, None, 0, "Cyan", "Goal", "", "memo1", 0, datetime.date.today()])
        task.append(["Fried Potato", prj4_ids[1], "Administrator", "TODO", 2, "Yes", datetime.date(2025, 8, 1), datetime.date(2025, 12, 1), 60, None, None, 0, "Cyan", "Goal", "", "memo1", 0, datetime.date.today()])
        task = {list_to_hash_w_ms(t[0:3]): t for t in task}
        task_ids = list(task.keys())

        todo = []
        todo.append(["Fry eggs", task_ids[0], "User", "TODO", 0, "Yes", None, None, 3, None, None, 0, "Red", "Goal", "", "memo", 0, datetime.date.today()])
        todo.append(["eat eggs", task_ids[0], "User", "TODO", 1, "Yes", None, None, 3, None, None, 0, "Red", "Goal", "", "memo", 0, datetime.date.today()])
        todo.append(["microwave", task_ids[1], "User", "TODO", 0, "Yes", None, None, 3, None, None, 0, "Red", "Goal", "", "memo", 0, datetime.date.today()])
        todo.append(["Chopped Onion", task_ids[4], "User", "TODO", 0, "Yes", None, None, 3, None, None, 0, "Red", "Goal", "", "memo", 0, datetime.date.today()])
        todo.append(["Knead", task_ids[4], "User", "TODO", 1, "Yes", None, None, 3, None, None, 0, "Red", "Goal", "", "memo", 0, datetime.date.today()])
        todo.append(["Bake", task_ids[4], "User", "TODO", 2, "Yes", None, None, 3, None, None, 0, "Red", "Goal", "", "memo", 0, datetime.date.today()])
        todo = {list_to_hash_w_ms(t[0:3]): t for t in todo}
        todo_ids = list(task.keys())

        SD = {}
        SD[1] = pd.DataFrame.from_dict(prj1, orient="index", columns=HEADERS)
        SD[2] = pd.DataFrame.from_dict(prj2, orient="index", columns=HEADERS)
        SD[3] = pd.DataFrame.from_dict(prj3, orient="index", columns=HEADERS)
        SD[4] = pd.DataFrame.from_dict(prj4, orient="index", columns=HEADERS)
        SD[5] = pd.DataFrame.from_dict(task, orient="index", columns=HEADERS)
        SD[6] = pd.DataFrame.from_dict(todo, orient="index", columns=HEADERS)

        for k, df in SD.items():
            print(k)
            print(df)
            print("")

        STATUS = ["TODO", "WIP", "DONE", "STORE", "CANCELED"]

        # Track Table
        DAILY_TABLE = [f"{i//4:02d}{(i%4)*15:02d}" for i in range(24*4)] + \
                      ["TOTAL", "FROM", "TO", "BREAK"]
        DAILY_ITEMS = ["Health", "Work_Place", "Safety", "OverWork", "Info1", "Info2", "Info3"]
        SD["daily_sch"] = pd.DataFrame(columns=DAILY_TABLE)
        SD["daily_info"] = pd.DataFrame(columns=DAILY_ITEMS)

        print(SD["daily_sch"])
        print()
        print(SD["daily_info"])
 
        save_schedule_data(SD, db_dir)