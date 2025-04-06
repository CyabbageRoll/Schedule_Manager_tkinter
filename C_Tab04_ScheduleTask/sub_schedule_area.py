from collections import OrderedDict, defaultdict, deque
import tkinter as tk
import datetime
from dateutil.relativedelta import relativedelta
import bisect
import pandas as pd
# user
import D_SubFrames as sf

class ScheduleArea(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.GP = master.GP
        self.OB = master.OB
        self.class_idx = 6
        self.owner = master.SP.user
        self.undraw_p_ids = set()
        self.width_scale = 10
        self.x00 = 10
        self.line_left_space = 15
        self.y00 = 10
        self.max_columns = 100
        self.dy = self.GP.schedule_font_size * self.GP.schedule_dy_factor
        self.color_dict = sf.generate_color_dict()
        self.on_canvas_items_idx = []
        self.on_canvas_items_y = []
        self.on_canvas_items = {}
        self.label_update_func = None
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()

    def set_variables(self):
        self.value = tk.StringVar()

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["canvas"] = tk.Canvas(self, bg=self.GP.schedule_bg_color, width=20000, height=10000)

    def pack_widgets(self):
        for k, widget in self.w.items():
            widget.pack(side=tk.LEFT, fill=tk.X, expand=False)

    def draw_corner(self):
        self.w["canvas"].create_text(0, 0, text="")

    def set_init(self):
        self.update(mode="both")
        
    def refresh_canvas_and_parameters(self):
        self.dy = self.GP.schedule_font_size * self.GP.schedule_dy_factor
        self.w["canvas"].delete("all")
        self.w["canvas"].configure(bg=self.GP.schedule_bg_color)
        self.draw_corner()

    def update(self, mode=None):
        """スケジュールエリアの更新
        Args:
            mode (str, optional): calender, width: カレンダの表示や幅を変える. prj: 描画するプロジェクトを更新. both: 両方. Defaults to None.
        """
        self.unbind()
        self.refresh_canvas_and_parameters()
        if mode in ["both", "calender", "width", "day_hour"]:
            self.create_calender_items()
        if mode in ["both", "prj"]:
            df_items = self.get_draw_items()
            self.sort_idx_hour_list = self.calc_start_limit(df_items)
        all_schedule_items = self.calculate_x_and_date_flag()
        self.draw_project_schedules(all_schedule_items)
        self.set_bind()

    def set_bind(self):
        for item_idx in self.on_canvas_items:
            self.w["canvas"].tag_bind(item_idx, "<Enter>",self.on_hover)
            self.w["canvas"].tag_bind(item_idx, "<Leave>",self.on_leave)

    def unbind(self):
        for item_idx in self.on_canvas_items:
            self.w["canvas"].tag_unbind(item_idx, "<Enter>")
            self.w["canvas"].tag_unbind(item_idx, "<Leave>")
        self.on_canvas_items = {}

    def on_hover(self, event):
        item = self.w["canvas"].find_withtag("current")
        if item:
            class_idx, idx = self.on_canvas_items[item[0]]
            name = self.SD[class_idx].loc[idx, "Name"]
            memo = self.SD[class_idx].loc[idx, "Memo"].replace("\n", " ")
            msg = f"{idx} : {name} - {memo}"
            self.label_update_func(msg)

    def on_leave(self, event):
        self.label_update_func("")

    def on_canvas_click(self, event):
        print("canvas is clicked")
        canvas = event.widget
        x, y = event.x, event.y
        item = canvas.find_closest(event.x, event.y)
        print(f"Clicked on item with text: {item}")

    def on_mouse_move(self, event):
        x, y = event.x, event.y
        msg = f"{x}, {y}"
        self.label_update_func(msg)

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

    # 順番にスケジュールを表示させる
    def draw_project_schedules(self, all_schedule_items):
        y0 = self.y00 * 1
        for p_id, schedule_items in all_schedule_items.items():
            y0 = self.draw_single_project_schedule(p_id, y0, schedule_items)

    # 1つの束のスケジュールを表示させる
    def draw_single_project_schedule(self, p_id, y0, schedule_items):
        # 親の表示
        df_p = self.SD[self.class_idx-1]
        ds_p = df_p.loc[p_id]
        names = self.get_parent_name(self.class_idx-1, p_id)
        ye = self.dy * (len(schedule_items) + 2)
        self.w["canvas"].create_line(self.x00, y0+self.dy/2, self.x00 + 10000, y0+self.dy/2,
                                     fill="#99AABB")
        self.w["canvas"].create_line(self.x00+self.line_left_space/2-1, y0-self.dy/2, self.x00+self.line_left_space/2-1, y0+ye,
                                     fill=self.color_dict[ds_p["Color"]],
                                     width=self.line_left_space-1)
        item_idx = self.w["canvas"].create_text(self.x00+self.line_left_space+2, y0, 
                                                text=names,
                                                anchor = "w",
                                                font=(self.GP.font_family, int(self.GP.schedule_font_size * self.GP.schedule_title_fontsize_factor)))
        self.on_canvas_items[item_idx] = (self.class_idx - 1, p_id)

        # カレンダー表示
        y0 += self.dy * 1
        ye = y0 + self.dy * (len(schedule_items) + 1)
        xs = self.x00 + self.line_left_space
        for x0, x1, str_dd in self.calender_items:
            self.w["canvas"].create_text(xs + (x0 + x1) / 2, y0, 
                                         text=str_dd, anchor="center",
                                         font=(self.GP.font_family, self.GP.schedule_font_size))
            self.w["canvas"].create_line(xs + x0, y0-self.dy/2, xs + x0, ye,
                                         fill="#99AABB")

            self.w["canvas"].create_line(self.x00 + self.line_left_space, y0+self.dy/2, self.x00+10000, y0+self.dy/2,
                                         fill="#99AABB")
            self.w["canvas"].create_line(self.x00 + self.line_left_space, ye, self.x00+10000, ye,
                                         fill="#99AABB")
        y0 += self.dy * 0.2

        # アイテム表示
        df = self.SD[self.class_idx]
        df = df[df["Parent_ID"] == p_id]
        for x0, x1, idx, available_flag, due_date_flag in schedule_items:
            ds = df.loc[idx]
            y0 += self.dy
            order_idx = f"[{int(ds['OrderValue'])}]"
            start_date = f"{ds['Plan_Begin_Date']} " if ds["Plan_Begin_Date"] else ""
            due_date = f"{ds['Plan_End_Date']}" if ds["Plan_End_Date"] else ""
            date_info = f": ({start_date} -> {due_date})" if start_date or due_date else ""
            hours = f" : {ds['Actual_Hour']}/{ds['Total_Estimate_Hour']} [hr]"
            text = f" {order_idx} {ds['Name']}" + hours + date_info
            color = "#FFBBEE" if due_date_flag else "#99BBBB"
            if available_flag and start_date:
                self.w["canvas"].create_line(x0 + self.line_left_space - 5, y0,
                                             x0 + self.line_left_space, y0,
                                             fill="#FF8888",
                                             width=self.dy)
            self.w["canvas"].create_line(x0 + self.line_left_space, y0,
                                         x1 + self.line_left_space, y0, 
                                         fill=color, 
                                         width=self.dy)
            self.w["canvas"].create_line(x0 + self.line_left_space, y0,
                                         x0 + self.line_left_space + 5, y0,
                                         fill=self.color_dict[ds["Color"]],
                                         width=self.dy)
            item_idx = self.w["canvas"].create_text(x0 + self.line_left_space + 5, y0, 
                                                    text=text, 
                                                    anchor="w",
                                                    font=(self.GP.font_family, self.GP.schedule_font_size))
            self.on_canvas_items[item_idx] = (self.class_idx, idx)
        return y0 + self.dy * 2
    
    def get_parent_name(self, class_idx, idx):
        names = []
        for i in range(class_idx):
            df = self.SD[self.class_idx - 1 - i]
            name, idx = df.loc[idx, ["Name", "Parent_ID"]]
            names.append(name)
        names = [n for n in names if n != "-"]
        if len(names) == 0:
            names = ["-"]
        name, p_names = names[0], names[1:]
        s = name + f" : "
        if p_names:
            s += " (" + " - ".join(p_names) + ") "
        return s
    
    def create_calender_items(self):
        w = self.SP.schedule_width * self.width_scale
        self.calender_items = []
        x0 = 0
        time_delta_dict = {"Daily": datetime.timedelta(days=1),
                           "Weekly": datetime.timedelta(weeks=1),
                           "Monthly": relativedelta(months=1)
                           }
        time_delta = time_delta_dict[self.SP.schedule_calender_type]
        dd = datetime.date.today()
        for _ in range(self.max_columns):
            x1 = x0 + w
            dd += time_delta
            str_dd = dd.strftime("%m/%d")
            self.calender_items.append((x0, x1, str_dd))
            x0 = x1

    def get_draw_items(self):
        p_ids = set(self.SD[self.class_idx-1].index.tolist())
        p_ids = [p_id for p_id in p_ids if p_id not in self.undraw_p_ids]
        df = self.SD[self.class_idx]
        df = df[df["Status"] == "ToDo"]
        if self.class_idx == 6:
            df = df[df["Owner"] == self.OB["Member"]]
        else:
            df = self.squeeze_user_related_df(df, self.OB["Member"], self.class_idx)
        df_items = {p_id: df[df["Parent_ID"] == p_id] for p_id in p_ids}
        return df_items
    
    def squeeze_user_related_df(self, df, member, class_idx):
        relative_ids = []
        for i in range(class_idx, 6):
            df_child = self.SD[6 - i + class_idx]
            df_parent = self.SD[5 - i + class_idx]
            # 子供の工数を足し合わせて親の工数を更新
            for idx in df_parent.index:
                df_child_tmp = df_child[df_child["Parent_ID"] == idx]
                estimate_hours = df_child_tmp["Total_Estimate_Hour"].sum()
                actual_hours = df_child_tmp["Actual_Hour"].sum()
                self.SD[5 - i + class_idx].loc[idx, "Total_Estimate_Hour"] = estimate_hours
                self.SD[5 - i + class_idx].loc[idx, "Actual_Hour"] = actual_hours
            # 子供の持ち主がmemberかもしくは、親の持ち主がmemberであるidxを抽出する
            df_child_1 = df_child[df_child["Owner"] == member]
            relative_ids1 = set(df_child_1["Parent_ID"].values.tolist())
            relative_ids2 = set(df_child.loc[relative_ids, "Parent_ID"].values.tolist())
            relative_ids3 = set(df_parent[df_parent["Owner"] == member].index.tolist())
            relative_ids = relative_ids1 | relative_ids2 | relative_ids3
        return df[df.index.isin(relative_ids)]

    # 並び替えて、日付をdatetime64に変換
    def arrange_df_with_order(self, df_items):
        for p_id, df in df_items.items():
            df = df.sort_values(by="OrderValue", ascending=False)
            for c in ["Plan_Begin_Date", "Plan_End_Date"]:
                df[c] = pd.to_datetime(df[c])
            df_items[p_id] = df
        return df_items

    def calc_start_limit(self, df_items):
        df_items = self.arrange_df_with_order(df_items)
        idx_hour_list = []
        # 親が同じ物事に開始しなければならない日を計算する
        available_start_hour_dict = {}
        tmp_estimate_hours = {}
        # 前から順番に開始可能な時間を計算する
        for p_id, df in df_items.items():
            next_available_start_hour = 0.0
            for idx in df.index[::-1]:
                tmp_estimate_hours[idx] = max(0.25, df.loc[idx, "Total_Estimate_Hour"] - df.loc[idx, "Actual_Hour"])
                available_start_hour_dict[idx] = next_available_start_hour
                start_date = df.loc[idx, "Plan_Begin_Date"]
                if start_date == start_date:
                    start_days = start_date.date() - datetime.date.today() - datetime.timedelta(days=1)
                    available_start_hour_dict[idx] = max(available_start_hour_dict[idx], start_days.days * self.SP.daily_task_hour)
                next_available_start_hour = available_start_hour_dict[idx] + tmp_estimate_hours[idx]

            # 後ろから順番に開始しなければならない時間を計算する
            must_start_hour = 9999
            for idx in df.index:
                remaining_hours1 = must_start_hour - tmp_estimate_hours[idx]
                # 自分自身の納期までの残り日数
                due_date = df.loc[idx, "Plan_End_Date"]
                remaining_hours2 = 9999
                if due_date == due_date:
                    remaining_days = due_date.date() - datetime.date.today()
                    remaining_hours2 = remaining_days.days * self.SP.daily_task_hour - tmp_estimate_hours[idx]
                must_start_hour = min(remaining_hours1, remaining_hours2)
                idx_hour_list.append((must_start_hour, available_start_hour_dict[idx], idx, p_id, tmp_estimate_hours[idx]))
        return sorted(idx_hour_list, reverse=True)


    def calculate_x_and_date_flag(self):
        all_schedule_items = defaultdict(list)
        x0, x1 = self.x00, self.x00
        column_days = {"Daily": 1, "Weekly": 5, "Monthly": 20}
        width_scale = self.SP.schedule_width * self.width_scale / (self.SP.daily_task_hour * column_days[self.SP.schedule_calender_type])
        current_hour = 0

        pop_list = {"base": self.sort_idx_hour_list.copy(), "waiting": deque()}
        while pop_list["base"] or pop_list["waiting"]:
            turn_name = self.which_turn(pop_list, current_hour)
            # リストの後ろから抽出し、baseから取り出してのてまだ開始できないものはwaitingに入れる
            must_start_hour, available_start_hour, idx, p_id, estimate_hour = pop_list[turn_name].pop()
            if turn_name == "base" and current_hour < available_start_hour:
                pop_list["waiting"].appendleft((must_start_hour, available_start_hour, idx, p_id, estimate_hour))
                continue

            due_date_flag = True if current_hour > must_start_hour else False
            available_flag = False
            if current_hour < available_start_hour:
                current_hour = available_start_hour
                x0 = current_hour * width_scale + self.x00
                available_flag = True
            x1 = x0 + estimate_hour * width_scale
            all_schedule_items[p_id].append((x0, x1, idx, available_flag, due_date_flag))
            x0 = x1 * 1
            current_hour += estimate_hour

            # print(f"current_hour: {current_hour:0.1f}, MH: {must_start_hour}, AH:{available_start_hour}, {self.SD[6].loc[idx, 'Name']}")
        return all_schedule_items


    def which_turn(self, pop_list, current_hour):
        # どちらのリストから抽出するかを決める
        if pop_list["waiting"] and pop_list["waiting"][-1][1] < current_hour:
            turn_name = "waiting"
        elif not pop_list["base"]:
            turn_name = "waiting"
        else:
            turn_name = "base"
        return turn_name



