from collections import OrderedDict
import tkinter as tk
import D_SubFrames as SF
import C_Tab04_ScheduleTask as tab4

class ScrollableScheduleArea(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.GP = master.GP
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
        self.w["area"] = tab4.ScheduleArea(self)
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
        self.w["area"].w["canvas"].bind("<ButtonPress-1>", self.start_drag)
        self.w["area"].w["canvas"].bind("<B1-Motion>", self.do_drag)

    def start_drag(self, event):
        # Save the last mouse position
        self.last_x = event.x
        self.last_y = event.y

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

    def update(self, mode):
        self.w["area"].update(mode)



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")
    root.SD = None
    root.SP = None
    root.logger = None
    root.font = ("Arial", 12)
    ss = ScrollableScheduleArea(root)
    ss.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
