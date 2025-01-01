from dataclasses import dataclass, asdict, field
from typing import List
import json
import os


@dataclass
class SettingParametersLocal:
    server_dir: str = r"../DB_DIR"
    user: str = "User"
    schedule_width = 10
    def __post_init__(self):
        pass


@dataclass
class SettingParametersServer:
    members: List[str] = field(default_factory=lambda: ["Member02", "Member03", "Member04", "Member05"])
    daily_begin_time: int = 6
    daily_end_time: int = 21
    daily_task_hour: int = 5
    schedule_draw_width: int = 10

@dataclass
class SettingParameters(SettingParametersServer, SettingParametersLocal):
    pass


@dataclass
class GUIParametersLocal:
    window_width: int = 1500
    window_height: int =1000
    font_size: int = 9
    font_family = "Meiryo"


@dataclass
class GUIParametersServer:
    window_bg_color: str = "#9e9e8e"


@dataclass
class GUIParameters(GUIParametersServer, GUIParametersLocal):
    pass


class JSONReadWrite:
    def __init__(self, local_dir, logger):
        self.local_dir = local_dir
        self.logger = logger

    def read(self):
        # localに置いている設定データの読み込み
        tmp_local = self._read_json(self.local_dir)
        assert tmp_local is not None, "'config.json was not FOUND'"
        SPL = SettingParametersLocal(**tmp_local["Setting"])
        GPL = GUIParametersLocal(**tmp_local["GUI"])
        # サーバーに置いている設定データの読み込み
        tmp_server = self._read_json(SPL.server_dir)
        if tmp_server is None:
            SPS = SettingParametersServer()
            GPS = GUIParametersServer()
            MEMO = self._white_memo()
        else:
            SPS = SettingParametersServer(**tmp_server["Setting"])
            GPS = GUIParametersServer(**tmp_server["GUI"])
        MEMO = self._read_json(SPL.server_dir)
        SP = SettingParameters(**vars(SPL), **vars(SPS))
        GP = GUIParameters(**vars(GPL), **vars(GPS))
        return SP, GP, MEMO

    def _read_json(self, p_dir):
        file_name = os.path.join(p_dir, "setting.json")
        if not os.path.exists(file_name):
            return None
        with open(file_name, encoding="UTF-8") as f:
            tmp = json.load(f)
        print
        return tmp

    def write(self, server_dir, SP=None, GP=None, MEMO=None):
        if MEMO is not None:
            self._write_json(server_dir, MEMO)
        if SP is not None and GP is not None:
            PL, PS = self._arrange_parameters(SP, GP)
            self._write_json(SP.server_dir, PS)
            self._write_json(self.local_dir, PL)

    def _write_json(self, p_dir, save_item):
        file_name = os.path.join(p_dir, "setting.json")
        with open(file_name, 'w', encoding="UTF-8") as f:
            json.dump(save_item, f, indent=4, ensure_ascii=False)

    def _white_memo(self):
        keys = ["Memo"]
        return {key: "" for key in keys}

    def _arrange_parameters(self, SP, GP):
        spl_keys = vars(SettingParametersLocal()).keys()
        sps_keys = vars(SettingParametersServer()).keys()
        gpl_keys = vars(GUIParametersLocal()).keys()
        gps_keys = vars(GUIParametersServer()).keys()

        sp_dic, gp_dic = vars(SP), vars(GP)
        SPL = {k: sp_dic[k] for k in spl_keys}
        SPS = {k: sp_dic[k] for k in sps_keys}
        GPL = {k: gp_dic[k] for k in gpl_keys}
        GPS = {k: gp_dic[k] for k in gps_keys}
        PL = {"Setting": SPL, "GUI": GPL}
        PS = {"Setting": SPS, "GUI": GPS}
        return PL, PS


if __name__ == "__main__":

    class L:
        def __init__(self):
            pass
        def debug(self, f):
            print(f)
        def info(self, f):
            print(f)

    logger = L()
    p_dir = os.path.dirname(os.path.dirname(__file__))
    json_wr = JSONReadWrite(p_dir, logger)
    SP, GP, MEMO = json_wr.read()
    print(f"{SP=}")
    print(f"{GP=}")
    print(f"{MEMO=}")

    print()
    json_wr.write(server_dir=SP.server_dir, SP=SP, GP=GP, MEMO=MEMO)