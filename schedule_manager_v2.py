# libraries
# default
import os
import tkinter as tk
import tkinter.font
from tkinter import ttk
import datetime

# user
import A_DataSettingRW as DS
import B_MainFrames as mf
import utils as ut


class ScheduleManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.VER = "v2-r20250406"
        self.logger = ut.logger_settings(add_info=self.VER)
        p_dir = os.path.dirname(__file__)
        self.json_rw = DS.JSONReadWrite(p_dir, self.logger)
        self.SP, self.GP, self.MEMO = self.json_rw.read()
        self.SD = DS.read_schedule_data(self.SP.server_dir)
        self.OB = {"Member": self.SP.user, "Date": datetime.date.today().strftime(r"%Y-%m-%d")}
        self.tk_setting()
        self.set_frames()
        self.grid_frames()
        self.set_binds()

    def tk_setting(self):
        self.font = tkinter.font.Font(self, family=self.GP.font_family, size=self.GP.font_size)
        self.title(f"Schedule App {self.VER}")
        self.geometry(f"{self.GP.window_width}x{self.GP.window_height}")
        self.configure(bg=self.GP.window_bg_color)

        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", font=self.font)
        s.configure("Treeview.Heading", font=self.font)
        s.configure("My.TButton", font=self.font, padding=[3, 3], background="white", foreground="black")
        s.configure("TNotebook.Tab", font=self.font, padding=[25, 5], foreground="white", background="gray")
        s.map("TNotebook.Tab", background=[("selected", "white"), ("disabled", "gray")],
                               foreground=[("selected", "black"), ("disabled", "white")],
                               padding=[("selected", [25, 5]), ("disabled", [25, 5])],)

    def set_frames(self):
        self.ob = mf.OptionBar(self, bg="#e09999", height=100, width=900)
        self.sw = mf.SubWindow(self, height=500, width=350)
        self.mw = mf.MainWindow(self, height=500, width=550)

    def grid_frames(self):
        self.ob.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        self.sw.grid(row=1, column=0, sticky=tk.NSEW)
        self.mw.grid(row=1, column=1, sticky=tk.NSEW)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def set_binds(self):
        self.sw.w["Project-Manage"].add_bind_func = self.refresh
        self.sw.w["Daily"].daily_schedule_update_bind = self.refresh
        self.sw.w["Daily"].daily_info_update_bind = self.refresh
        self.mw.w["ATT"].click_apply_bind = self.refresh
        self.mw.w["Schedule"].w["schedule"].click_bind_func = self.task_click
        self.mw.w["Schedule"].w["schedule"].edit_ticket_menu_click = self.edit_ticket
        self.mw.w["Schedule"].w["schedule"].edit_att_menu_click = self.edit_att
        self.mw.w["Schedule"].w["schedule"].status_update = self.status_update
        self.mw.w["Regularly"].w["regularly"].click_bind_func = self.task_click
        self.mw.w["Regularly"].w["regularly"].edit_ticket_menu_click = self.edit_ticket
        self.mw.w["Regularly"].w["regularly"].edit_att_menu_click = self.edit_att
        self.mw.w["Regularly"].w["regularly"].status_update = self.status_update
        self.mw.w["Recent"].w["recent"].edit_ticket_menu_click = self.edit_ticket
        self.mw.w["Recent"].w["recent"].edit_att_menu_click = self.edit_att
        self.mw.w["Recent"].w["recent"].status_update = self.status_update
        self.mw.w["Projects-Display"].edit_ticket_menu_click = self.edit_ticket
        self.mw.w["Projects-Display"].edit_att_menu_click = self.edit_att
        self.ob.get_memo_dict = self.mw.w["Memo"].get_to_memo_dict
        self.ob.refresh_bind_func = self.refresh

    def edit_ticket(self, class_idx, idx):
        self.sw.w["Project-Manage"].set(class_idx, idx)
        self.sw.select(self.sw.w["Project-Manage"])

    def edit_att(self, class_idx, idx):
        self.mw.w["ATT"].set(class_idx, idx)
        self.mw.select(self.mw.w["ATT"])

    def task_click(self, class_idx, idx):
        current_tab = self.sw.select()
        if class_idx == 6:
            if current_tab == ".!subwindow.!dailyinformation":
                ds = self.SD[class_idx].loc[idx, :]
                self.sw.w["Daily"].update_item(ds)

    def status_update(self, class_idx, idx, status):
        self.SD[class_idx].loc[idx, "Status"] = status
        self.refresh()

    def refresh(self):
        self.logger.debug("refresh")
        self.mw.w["Schedule"].update()
        self.mw.w["Regularly"].update()
        self.mw.w["Recent"].update()
        self.mw.w["Projects-Display"].refresh_button_press()
        self.sw.w["Daily"].refresh()
        self.mw.w["Team"].refresh()
        self.sw.w["Project-Manage"].w["Selector"].update_list_box()
        self.mw.w["ATT"].w["selector"].update_list_box()
        # self.w["Project-Manage"].refresh()
        # self.w["ATT"].refresh()
        # self.w["Goals/Reflections"].refresh()
        # self.w["Follows"].refresh()


if __name__ == "__main__":
    sch_app = ScheduleManager()
    sch_app.mainloop()
    sch_app.logger.debug("Application Ends")