import tkinter as tk

class ResizableCanvas(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create a canvas
        self.canvas = tk.Canvas(self, bg="white")

        # Create vertical scrollbar
        self.scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Create horizontal scrollbar
        self.scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure canvas to use scrollbars
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Create a frame to hold the contents of the canvas
        self.content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Bind events to update scroll region
        self.content_frame.bind("<Configure>", self.update_scroll_region)

    def update_scroll_region(self, event):
        # Update the scroll region to encompass the entire content frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class ScheduleArea(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = ResizableCanvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Add items to the canvas
        for i in range(50):  # Create multiple items to exceed the viewable area
            tk.Label(self.canvas.content_frame, text=f"Item {i + 1}", width=20, height=2, bg="lightgray").grid(row=i, column=0, pady=5)

        # Add additional items for horizontal scrolling
        for j in range(30):  # Adding more items for horizontal overflow
            tk.Label(self.canvas.content_frame, text=f"Column {j + 1}", width=20, height=2, bg="lightblue").grid(row=0, column=j, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Set initial window size
    app = ScheduleArea(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
