from collections import OrderedDict
import tkinter as tk
import D_SubFrames as SF
import C_Tab09_Recent as tab9

class ScrollableRecentArea(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.GP = master.GP
        self.OB = master.OB
        self.click_bind_func = None
        self.edit_ticket_menu_click = None
        self.edit_att_menu_click = None
        self.status_update = None
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

        # Initialize variables for dragging
        self.last_x = None
        self.last_y = None

    def set_variables(self):
        self.value = tk.StringVar()

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["area"] = tab9.RecentArea(self)
        self.w["scroll_h"] = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.w["area"].w["canvas"].xview)
        self.w["scroll_v"] = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.w["area"].w["canvas"].yview)
        self.w["area"].w["canvas"].configure(xscrollcommand=self.w["scroll_h"].set)
        self.w["area"].w["canvas"].configure(yscrollcommand=self.w["scroll_v"].set)

    def pack_widgets(self):
        self.w["area"].grid(row=0, column=0, sticky=tk.NSEW)
        self.w["scroll_h"].grid(row=1, column=0, sticky=tk.EW)
        self.w["scroll_v"].grid(row=0, column=1, sticky=tk.NS)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def set_init(self):
        self.update_scrollregion()

    def update_scrollregion(self):
        self.w["area"].w["canvas"].update_idletasks()
        self.w["area"].w["canvas"].configure(scrollregion=self.w["area"].w["canvas"].bbox("all"))

    def set_bind(self):
        # Bind mouse drag events for scrolling
        # return
        self.w["area"].w["canvas"].bind("<ButtonPress-1>", self.mouse_click)
        self.w["area"].w["canvas"].bind("<ButtonPress-2>", self.mouse_click_right)
        self.w["area"].w["canvas"].bind("<ButtonPress-3>", self.mouse_click_right)
        self.w["area"].w["canvas"].bind("<B1-Motion>", self.do_drag)
        self.w["area"].w["canvas"].bind("<MouseWheel>", self.mouse_wheel)
        self.w["area"].w["canvas"].bind("<Alt-MouseWheel>", self.alt_mouse_wheel)

    def mouse_click(self, event):
        self.last_x = event.x
        self.last_y = event.y

        item = self.w["area"].w["canvas"].find_withtag("current")
        # if item:
        #     class_idx, idx = self.w["area"].on_canvas_items[item[0]]
        #     self.click_bind_func(class_idx, idx)

    def mouse_click_right(self, event):
        item = self.w["area"].w["canvas"].find_withtag("current")
        if not item:
            return
        class_idx, idx = self.w["area"].on_canvas_items.get(item[0], [None, None])
        if class_idx:
            self.show_menu(event, class_idx, idx)

    def show_menu(self, event, class_idx, idx):
        # メニューを指定した位置に表示
        popup_menu = tk.Menu(self, tearoff=0)
        # popup_menu.add_command(label="編集", command=lambda : self.edit_ticket_menu_click(class_idx, idx))
        # popup_menu.add_command(label="ATT", command=lambda : self.edit_att_menu_click(class_idx, idx))
        # popup_menu.add_separator()
        popup_menu.add_command(label="Done", command=lambda : self.status_update(class_idx, idx, "Done"))
        popup_menu.add_command(label="Cancel", command=lambda : self.status_update(class_idx, idx, "Cancel"))
        popup_menu.add_command(label="Regularly", command=lambda : self.status_update(class_idx, idx, "Regularly"))
        popup_menu.add_command(label="ToDo", command=lambda : self.status_update(class_idx, idx, "ToDo"))
        popup_menu.post(event.x_root, event.y_root)

    def do_drag(self, event):
        # Check if Control key is pressed
        if event.state & 0x0004:  # Control key is pressed
            delta_x = self.last_x - event.x
            delta_y = self.last_y - event.y

            # Scroll the canvas based on the mouse drag distance
            self.w["area"].w["canvas"].xview_scroll(int(delta_x / 10), "units")
            self.w["area"].w["canvas"].yview_scroll(int(delta_y / 10), "units")

            # Update the last mouse position
            self.last_x = event.x
            self.last_y = event.y

    def mouse_wheel(self, event):
        self.w["area"].w["canvas"].yview_scroll(int(-1*(event.delta/120)), "units")

    def alt_mouse_wheel(self, event):
        self.w["area"].w["canvas"].yview_scroll(int(-1*(event.delta/120)), "units")

    def update(self, display_date, mode):
        self.w["area"].update(display_date, mode)


