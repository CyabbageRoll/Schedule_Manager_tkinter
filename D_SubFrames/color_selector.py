from collections import OrderedDict
import tkinter as tk
from tkinter import ttk


class ColorSelector(tk.Frame):
    def __init__(self, master, init_color="Cyan", **kwargs):
        super().__init__(master, **kwargs)
        self.logger = master.logger
        self.font = master.font
        self.color_dict = generate_color_dict()
        self.color_dict_to_name = {v: k for k, v in self.color_dict.items()}
        self.add_bind_func = None
        init_color = init_color if init_color[0] != "#" else self.color_dict_to_name[init_color]
        self.set_variables()
        self.set_widgets()
        self.pack_widgets()
        self.set_init(init_color)
        self.set_bind()

    def set_variables(self):
        self.label = tk.StringVar()
        self.display_color = tk.StringVar()
        self.color_list = list(self.color_dict.keys())

    def set_widgets(self):
        self.w = OrderedDict()
        self.w["Combobox"] = ttk.Combobox(self,
                                          textvariable=self.display_color,
                                          values=self.color_list,
                                          width=10,
                                          height=10,
                                          font=self.font,
                                          state="readonly")
        self.w["ColorDisplay"] = tk.Label(self, width=2)

    def pack_widgets(self):
        for key, widget in self.w.items():
            f = tk.BOTH if key == "Combobox" else tk.Y
            e = True if key == "Combobox" else False
            widget.pack(side=tk.LEFT, fill=f, expand=e)

    def set_init(self, init_color):
        self.display_color.set(init_color)
        self.on_select(None)

    def set_bind(self):
        self.w["Combobox"].bind("<<ComboboxSelected>>", self.on_select)

    def on_select(self, event):
        color_str = self.get()
        self.update_label_color(color_str)
        if self.add_bind_func:
            self.add_bind_func()

    def update_label_color(self, color_str):
        if not color_str:
            color_str = "White"
        self.w["ColorDisplay"].config(bg=self.color_dict[color_str])

    def set(self, color_str):
        self.display_color.set(color_str)
        self.update_label_color(color_str)

    def get(self):
        return self.display_color.get()

    def get_as_hex(self):
        color_name = self.get()
        return self.color_dict[color_name]


def generate_color_dict():
    colors = {}
    colors["IndianRed"] = "#CD5C5C"
    colors["LightCoral"] = "#F08080"
    colors["Salmon"] = "#FA8072"
    colors["DarkSalmon"] = "#E9967A"
    colors["LightSalmon"] = "#FFA07A"
    colors["Crimson"] = "#DC143C"
    colors["Red"] = "#FF0000"
    colors["FireBrick"] = "#B22222"
    colors["DarkRed"] = "#8B0000"
    colors["Pink"] = "#FFC0CB"
    colors["LightPink"] = "#FFB6C1"
    colors["HotPink"] = "#FF69B4"
    colors["DeepPink"] = "#FF1493"
    colors["MediumVioletRed"] = "#C71585"
    colors["PaleVioletRed"] = "#DB7093"
    colors["Coral"] = "#FF7F50"
    colors["Tomato"] = "#FF6347"
    colors["OrangeRed"] = "#FF4500"
    colors["DarkOrange"] = "#FF8C00"
    colors["Orange"] = "#FFA500"
    colors["Gold"] = "#FFD700"
    colors["Yellow"] = "#FFFF00"
    colors["LightYellow"] = "#FFFFE0"
    colors["LemonChiffon"] = "#FFFACD"
    colors["LightGoldenrodYellow"] = "#FAFAD2"
    colors["PapayaWhip"] = "#FFEFD5"
    colors["Moccasin"] = "#FFE4B5"
    colors["PeachPuff"] = "#FFDAB9"
    colors["PaleGoldenrod"] = "#EEE8AA"
    colors["Khaki"] = "#F0E68C"
    colors["DarkKhaki"] = "#BDB76B"
    colors["Lavender"] = "#E6E6FA"
    colors["Thistle"] = "#D8BFD8"
    colors["Plum"] = "#DDA0DD"
    colors["Violet"] = "#EE82EE"
    colors["Orchid"] = "#DA70D6"
    colors["Fuchsia"] = "#FF00FF"
    colors["Magenta"] = "#FF00FF"
    colors["MediumOrchid"] = "#BA55D3"
    colors["MediumPurple"] = "#9370DB"
    colors["Amethyst"] = "#9966CC"
    colors["BlueViolet"] = "#8A2BE2"
    colors["DarkViolet"] = "#9400D3"
    colors["DarkOrchid"] = "#9932CC"
    colors["DarkMagenta"] = "#8B008B"
    colors["Purple"] = "#800080"
    colors["Indigo"] = "#4B0082"
    colors["SlateBlue"] = "#6A5ACD"
    colors["DarkSlateBlue"] = "#483D8B"
    colors["GreenYellow"] = "#ADFF2F"
    colors["Chartreuse"] = "#7FFF00"
    colors["LawnGreen"] = "#7CFC00"
    colors["Lime"] = "#00FF00"
    colors["LimeGreen"] = "#32CD32"
    colors["PaleGreen"] = "#98FB98"
    colors["LightGreen"] = "#90EE90"
    colors["MediumSpringGreen"] = "#00FA9A"
    colors["SpringGreen"] = "#00FF7F"
    colors["MediumSeaGreen"] = "#3CB371"
    colors["SeaGreen"] = "#2E8B57"
    colors["ForestGreen"] = "#228B22"
    colors["Green"] = "#008000"
    colors["DarkGreen"] = "#006400"
    colors["YellowGreen"] = "#9ACD32"
    colors["OliveDrab"] = "#6B8E23"
    colors["Olive"] = "#808000"
    colors["DarkOliveGreen"] = "#556B2F"
    colors["MediumAquamarine"] = "#66CDAA"
    colors["DarkSeaGreen"] = "#8FBC8F"
    colors["LightSeaGreen"] = "#20B2AA"
    colors["DarkCyan"] = "#008B8B"
    colors["Teal"] = "#008080"
    colors["Aqua"] = "#00FFFF"
    colors["Cyan"] = "#00FFFF"
    colors["LightCyan"] = "#E0FFFF"
    colors["PaleTurquoise"] = "#AFEEEE"
    colors["Aquamarine"] = "#7FFFD4"
    colors["Turquoise"] = "#40E0D0"
    colors["MediumTurquoise"] = "#48D1CC"
    colors["DarkTurquoise"] = "#00CED1"
    colors["CadetBlue"] = "#5F9EA0"
    colors["SteelBlue"] = "#4682B4"
    colors["LightSteelBlue"] = "#B0C4DE"
    colors["PowderBlue"] = "#B0E0E6"
    colors["LightBlue"] = "#ADD8E6"
    colors["SkyBlue"] = "#87CEEB"
    colors["LightSkyBlue"] = "#87CEFA"
    colors["DeepSkyBlue"] = "#00BFFF"
    colors["DodgerBlue"] = "#1E90FF"
    colors["CornflowerBlue"] = "#6495ED"
    colors["MediumSlateBlue"] = "#7B68EE"
    colors["RoyalBlue"] = "#4169E1"
    colors["Blue"] = "#0000FF"
    colors["MediumBlue"] = "#0000CD"
    colors["DarkBlue"] = "#00008B"
    colors["Navy"] = "#000080"
    colors["MidnightBlue"] = "#191970"
    colors["Cornsilk"] = "#FFF8DC"
    colors["BlanchedAlmond"] = "#FFEBCD"
    colors["Bisque"] = "#FFE4C4"
    colors["NavajoWhite"] = "#FFDEAD"
    colors["Wheat"] = "#F5DEB3"
    colors["BurlyWood"] = "#DEB887"
    colors["Tan"] = "#D2B48C"
    colors["RosyBrown"] = "#BC8F8F"
    colors["SandyBrown"] = "#F4A460"
    colors["Goldenrod"] = "#DAA520"
    colors["DarkGoldenrod"] = "#B8860B"
    colors["Peru"] = "#CD853F"
    colors["Chocolate"] = "#D2691E"
    colors["SaddleBrown"] = "#8B4513"
    colors["Sienna"] = "#A0522D"
    colors["Brown"] = "#A52A2A"
    colors["Maroon"] = "#800000"
    colors["White"] = "#FFFFFF"
    colors["Snow"] = "#FFFAFA"
    colors["Honeydew"] = "#F0FFF0"
    colors["MintCream"] = "#F5FFFA"
    colors["Azure"] = "#F0FFFF"
    colors["AliceBlue"] = "#F0F8FF"
    colors["GhostWhite"] = "#F8F8FF"
    colors["WhiteSmoke"] = "#F5F5F5"
    colors["Seashell"] = "#FFF5EE"
    colors["Beige"] = "#F5F5DC"
    colors["OldLace"] = "#FDF5E6"
    colors["FloralWhite"] = "#FFFAF0"
    colors["Ivory"] = "#FFFFF0"
    colors["AntiqueWhite"] = "#FAEBD7"
    colors["Linen"] = "#FAF0E6"
    colors["LavenderBlush"] = "#FFF0F5"
    colors["MistyRose"] = "#FFE4E1"
    colors["Gainsboro"] = "#DCDCDC"
    colors["LightGrey"] = "#D3D3D3"
    colors["Silver"] = "#C0C0C0"
    colors["DarkGray"] = "#A9A9A9"
    colors["Gray"] = "#808080"
    colors["DimGray"] = "#696969"
    colors["LightSlateGray"] = "#778899"
    colors["SlateGray"] = "#708090"
    colors["DarkSlateGray"] = "#2F4F4F"
    colors["Black"] = "#000000"
    return colors
