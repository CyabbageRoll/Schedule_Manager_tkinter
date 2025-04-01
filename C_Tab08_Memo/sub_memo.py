# default
from collections import OrderedDict
import tkinter as tk

# user
import D_SubFrames as sf


class TeamInfo(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.SD = master.SD
        self.SP = master.SP
        self.OB = master.OB
        self.MEMO = master.MEMO
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init()
        self.set_bind()

    def set_variables(self):
        pass

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["Memo"] = tk.Text(self, font=self.font)

    def pack_widgets(self):
        self.w["Memo"].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def refresh(self):
        self.set_memo()

    def set_init(self):
        self.refresh()

    def set_bind(self):
        self.w["Memo"].bind("<Return>", self.press_key)
        self.w["Memo"].bind("<FocusOut>", self.press_key)

    def set_new_text(self, txt):
        self.w[f"Memo"].delete("1.0", tk.END)
        self.w[f"Memo"].insert(tk.END, txt)

    def set_memo(self):
        memo_txt = self.MEMO["Memo"]
        # print(f"{memo_txt=}")
        # print(f"{memo_txt[-1:]=}")
        while len(memo_txt) > 2 and memo_txt[-1:] == "\n":
            memo_txt = memo_txt[:-1]
        # print(f"{memo_txt=}")
        self.set_new_text(memo_txt)

    def press_key(self, event):
        self.get_to_memo_dict()

    def get_to_memo_dict(self):
        txt = self.w["Memo"].get("1.0", tk.END)
        self.MEMO["Memo"] = txt
        self.logger.debug(f"memo updated")
