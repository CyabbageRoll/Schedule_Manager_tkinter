from collections import OrderedDict
import tkinter as tk
import datetime
import pandas as pd


class ScheduleArea(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.class_idx = 6
        self.owner = master.SP.user
        self.undraw_p_ids = set()
        self.width_scale = 10
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        self.value = tk.StringVar()

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["canvas"] = tk.Canvas(self, bg="gray", width=20000, height=1000)
        pass

    def pack_widgets(self):
        for k, widget in self.w.items():
            widget.pack(side=tk.LEFT, fill=tk.X, expand=False)

    def set_init(self):
        # self.w["canvas"].create_text(100, 100, text="aaa")
        self.w["canvas"].create_text(1000, 1000, text="aaa")
        self.arrange_data_and_draw_schedules()
        pass

    def update(self, v):
        print(f"{self.SP.font_size=}")
        print(f"{self.SP.schedule_width=}")
        pass

    def set_bind(self):
        pass

    def set_project(self):
        pass

    def set_p_ids(self, ids:list):
        pass

    def remove_p_ids(self, ids:list):
        pass

    def set_owner(self, owner):
        pass

    def get(self):
        pass

    # スケジュールを表示させる親メソッド
    def arrange_data_and_draw_schedules(self):
        df_items = self.get_draw_items()
        idx_remaining_hour = self.calc_start_limit(df_items)
        all_schedule_items = self.calculate_x(idx_remaining_hour)
        calender_type = "date"
        calender_items = self.create_calender_items(calender_type)
        self.draw_project_schedules(all_schedule_items, calender_items)
        pass

    # 順番にスケジュールを表示させる
    def draw_project_schedules(self, all_schedule_items, calender_items):
        for schedule_items in all_schedule_items:
            self.draw_single_project_schedule("test", 100, calender_items, schedule_items)

    def draw_single_project_schedule(self, title, y0, calender_items, schedule_items):
        x00 = 100
        self.w["canvas"].create_text(x00, y0, text=title, font=("Meiryo", 20))
        for x0, x1, str_dd in calender_items:
            self.w["canvas"].create_text(x00+(x0+x1)//2, y0+10, text=str_dd, font=("Meiryo", 8))

    def create_calender_items(self, calender_type):
        if calender_type == "date":
            calender_item = self.create_date_items(100, 10)
        return calender_item

    def create_date_items(self, max_columns, column_width):
        w = self.SP.schedule_width * column_width
        date_items = []
        x0 = 0
        for i in range(max_columns):
            x1 = x0 + w
            dd = datetime.date.today() + datetime.timedelta(days=i)
            str_dd = dd.strftime("%m/%d")
            date_items.append((x0, x1, str_dd))
            x0 = x1
        return date_items

    def get_draw_items(self):
        p_ids = set(self.SD[self.class_idx-1].index.tolist())
        p_ids = [p_id for p_id in p_ids if p_id not in self.undraw_p_ids]
        df = self.SD[self.class_idx]
        df = df[df["Status"] == "TODO"]
        df = df[df["Owner"] == self.owner]
        df_items = {p_id: df[df["Parent_ID"] == p_id] for p_id in p_ids}
        return df_items

    # 並び替えて、日付をdatetime64に変換
    def arrange_df_with_order(self, df_items):
        for p_id, df in df_items.items():
            df = df.sort_values(by="Order", ascending=False)
            for c in ["Plan_Begin_Date", "Plan_End_Date"]:
                df[c] = pd.to_datetime(df[c])
            df_items[p_id] = df
        return df_items

    def calc_start_limit(self, df_items):
        df_items = self.arrange_df_with_order(df_items)
        idx_remaining_hour = []
        for p_id, df in df_items.items():
            remaining_hour = 9999
            for idx in df.index:
                r1 = remaining_hour - df.loc[idx, "Total_Estimate_Hour"]
                due_date = df.loc[idx, "Plan_End_Date"]
                if due_date == due_date:
                    r2 = due_date.date() - datetime.date.today()
                    r2 = r2.days * self.SP.daily_task_hour
                else:
                    r2 = 9999
                remaining_hour = min(r1, r2)
                idx_remaining_hour.append((remaining_hour, idx, p_id))
        print(f"{idx_remaining_hour=}")
        return idx_remaining_hour


    def calculate_x(self, idx_remaining_hour):
        w = self.SP.schedule_width * self.width_scale
        self.SP.daily_task_hour
        return [1]

    def calculate_y(self):
        pass


