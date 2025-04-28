from collections import OrderedDict, defaultdict
import tkinter as tk
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
# user
import D_SubFrames as sf

class RegularlyArea(tk.Frame):
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
        self.update()
        
    def refresh_canvas_and_parameters(self):
        self.dy = self.GP.schedule_font_size * self.GP.schedule_dy_factor
        self.w["canvas"].delete("all")
        self.w["canvas"].configure(bg=self.GP.schedule_bg_color)
        self.draw_corner()

    def update(self, mode=None):
        """スケジュールエリアの更新
        Args:
            mode (str, optional):
        """
        self.unbind()
        self.refresh_canvas_and_parameters()
        df_items = self.get_draw_items()
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
        sorted_idx = self.sort_task_ids(all_schedule_items.keys())
        for p_id in sorted_idx:
            y0 = self.draw_single_project_schedule(p_id, y0, all_schedule_items[p_id])

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
                                                font=(self.GP.font_family, int(self.GP.schedule_font_size * self.GP.schedule_title_fontsize_factor), "bold"))
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
        s = ""
        if p_names:
            s += " - ".join(p_names[::-1])
            s += f" - "
        s += name
        return s

    def get_parent_indices_and_name(self, class_idx, idx):
        p2c_dic_single = {}
        for i in range(class_idx):
            df = self.SD[self.class_idx - 1 - i]
            name, pid = df.loc[idx, ["Name", "Parent_ID"]]
            p2c_dic_single[pid] = (idx, name)
            idx = pid
        return p2c_dic_single
    
    def get_draw_items(self):
        p_ids = set(self.SD[self.class_idx-1].index.tolist())
        p_ids = [p_id for p_id in p_ids if p_id not in self.undraw_p_ids]
        df = self.SD[self.class_idx]
        df = df[df["Status"] == "Regularly"]
        df = df[df["Owner"] == self.OB["Member"]]
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
    
    def sort_task_ids(self, task_ids):
        p2c_dic = defaultdict(list)
        for task_id in task_ids:
            p2c_dic_single = self.get_parent_indices_and_name(class_idx=self.class_idx-1, idx=task_id)
            for pid, (idx, name) in p2c_dic_single.items():
                p2c_dic[pid].append((name, idx))
        
        sorted_idx = []
        search_list = sorted(list(set(p2c_dic["0"])))
        while search_list:
            name, idx = search_list.pop()
            if idx in task_ids:
                sorted_idx.append((idx))
            else:
                search_list.extend(sorted(list(set(p2c_dic.get(idx, [])))))
        return sorted_idx