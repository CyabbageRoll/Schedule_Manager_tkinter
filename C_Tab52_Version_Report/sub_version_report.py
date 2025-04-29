# default
from collections import OrderedDict
import tkinter as tk

# user
import D_SubFrames as sf


class Version_Report(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.OB = master.OB
        self.INFO = master.INFO
        self.MEMO = master.MEMO
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        self.message = tk.StringVar()

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["Label1"] = tk.Label(self, text="■ 更新情報", font=self.font, justify="left", anchor="w")
        self.w["Report"] = tk.Text(self, font=self.font, height=10)
        self.w["Space1"] = tk.Label(self, text=" ", font=self.font, justify="left", anchor="w")
        self.w["Label2"] = tk.Label(self, text="■ バグ、改善要望記入", font=self.font, justify="left", anchor="w")
        self.w["BugReport"] = tk.Text(self, font=self.font, height=10)

    def pack_widgets(self):
        for k, widget in self.w.items():
            f = tk.BOTH
            e = True if k == "Report" else False
            widget.pack(side=tk.TOP, fill=f, expand=e)

    def refresh(self):
        self.set_memo()

    def set_init(self):
        # self.message.set(self.get_arrange_message())
        self.set_version_info()
        self.refresh()

    def get_arrange_message(self):
        message =self.INFO["Versions"]
        arr_msg = ""
        for ver, txt_dic in message.items():
            arr_msg += f"   - {ver}\n"
            for txt in txt_dic.values():
                arr_msg += f"      ・{txt}\n"
        return arr_msg

    def set_bind(self):
        self.w["BugReport"].bind("<Return>", self.press_key)
        self.w["BugReport"].bind("<FocusOut>", self.press_key)

    def set_new_text(self, txt):
        self.w[f"BugReport"].delete("1.0", tk.END)
        self.w[f"BugReport"].insert(tk.END, txt)

    def set_memo(self):
        memo_txt = self.INFO.get("Report", "")
        while len(memo_txt) > 2 and memo_txt[-1:] == "\n":
            memo_txt = memo_txt[:-1]
        self.set_new_text(memo_txt)

    def press_key(self, event):
        self.get_to_memo_dict()

    def get_to_memo_dict(self):
        txt = self.w["BugReport"].get("1.0", tk.END)
        self.INFO["Report"] = txt
        self.logger.debug(f"memo updated")

    def set_version_info(self):
        msg = self.get_arrange_message()
        self.w[f"Report"].delete("1.0", tk.END)
        self.w[f"Report"].insert(tk.END, msg)