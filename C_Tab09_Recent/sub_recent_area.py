from collections import OrderedDict, defaultdict
import tkinter as tk
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
# user
import D_SubFrames as sf

class RecentArea(tk.Frame):
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
        self.width_scale = 5
        self.x00 = 10
        self.line_left_space = 30
        self.y00 = 10
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
        t = datetime.date.today()
        self.update((t, t))
        
    def refresh_canvas_and_parameters(self):
        self.dy = self.GP.schedule_font_size * self.GP.schedule_dy_factor
        self.w["canvas"].delete("all")
        self.w["canvas"].configure(bg=self.GP.schedule_bg_color)
        self.draw_corner()

    def update(self, display_date, mode=None):
        """スケジュールエリアの更新
        Args:
            mode (str, optional):
        """
        self.unbind()
        self.refresh_canvas_and_parameters()
        df_items = self.get_draw_items(display_date)
        all_schedule_items = self.arrange_df_hours(df_items)
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
            msg = f"{idx} : {name} {event.y}"
            self.label_update_func(msg)

    def on_leave(self, event):
        self.label_update_func("")

    def on_canvas_click(self, event):
        print("canvas is clicked")
        canvas = event.widget
        x, y = event.x, event.y
        print(x, y)
        item = canvas.find_closest(event.x, event.y)
        print(f"Clicked on item with text: {item}")

    def on_mouse_move(self, event):
        x, y = event.x, event.y
        msg = f"{x}, {y}"
        self.label_update_func(msg)
        print(x, y)

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
        item_idx = self.w["canvas"].create_text(self.x00+5, y0, 
                                                text=names,
                                                anchor = "w",
                                                font=(self.GP.font_family, int(self.GP.schedule_font_size * self.GP.schedule_title_fontsize_factor)))
        self.on_canvas_items[item_idx] = (self.class_idx - 1, p_id)

        # アイテム表示
        df = self.SD[self.class_idx]
        df = df[df["Parent_ID"] == p_id]
        for x0, x1, idx in schedule_items:
            ds = df.loc[idx]
            y0 += self.dy
            hours = f" : {ds['Actual_Hour']} [hr]"
            text = f"{ds['Name']}" + hours
            self.w["canvas"].create_line(x0 + self.line_left_space, y0,
                                         x1 + self.line_left_space, y0, 
                                         fill="#FFBBEE", 
                                         width=self.dy*0.9)
            self.w["canvas"].create_line(x0 + self.line_left_space, y0,
                                         x0 + self.line_left_space + 5, y0,
                                         fill=self.color_dict[ds["Color"]],
                                         width=self.dy*0.9)
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
    
    def get_draw_items(self, display_date):
        from_date, to_date = display_date
        day_count = (to_date - from_date).days
        display_date_list = [from_date + datetime.timedelta(days=i) for i in range(day_count + 1)]
        print(display_date_list)
        display_date_indices = [str(d) + "-" + self.OB["Member"] for d in display_date_list]
        print(display_date_indices)
        display_items = defaultdict(int)
        daily_column_name_list = [f"C{i//4:02d}{(i%4)*15:02d}" for i in range(24*4)]
        for sch_idx in display_date_indices:
            if sch_idx in self.SD["daily_sch"].index:
                for idx in self.SD["daily_sch"].loc[sch_idx, daily_column_name_list]:
                    if idx:
                        display_items[idx] += 0.25

        df = self.SD[6].loc[display_items.keys(), :]
        p_ids = df["Parent_ID"].unique()
        df_items = {p_id: df[df["Parent_ID"] == p_id] for p_id in p_ids}
        return df_items

    def arrange_df_hours(self, df_items):
        all_schedule_items = defaultdict(list)
        for p_id, df in df_items.items():
            df = df.sort_values(by="Actual_Hour", ascending=False)
            for idx in df.index:
                x1 = self.x00 + df.loc[idx, "Actual_Hour"] * self.width_scale
                all_schedule_items[p_id].append((self.x00, x1, idx))
        return all_schedule_items
    

