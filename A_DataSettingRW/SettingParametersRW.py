from dataclasses import dataclass, asdict, field
from typing import List
import json
import os


@dataclass
class SettingParametersLocal:
    server_dir: str = r"../DB_DIR"
    def __post_init__(self):
        pass


@dataclass
class SettingParametersServer:
    user: str = "User"
    members: List[str] = field(default_factory=lambda: ["User"])
    daily_begin_time: int = 6
    daily_end_time: int = 21
    daily_task_hour: int = 5
    schedule_width: int = 10
    schedule_draw_width: int = 10
    schedule_prj_type: str = 6
    schedule_calendar_type: str = "Daily"
    schedule_display_type: str = "Gantt"
    schedule_start_date: str = "2025-04-01"
    schedule_holidays: List[str] = field(default_factory=lambda: ["SUN", "SAT"])
    daily_info_combo_Health: List[str] = field(default_factory=lambda: ["Good", "Bad"])
    daily_info_combo_Work_Place: List[str] = field(default_factory=lambda: ["Office", "Home"])
    daily_info_combo_Safety: List[str] = field(default_factory=lambda: [])
    daily_info_combo_OverWork: List[str] = field(default_factory=lambda: [])
    command_buttons: List[str] = field(default_factory=lambda: ["Command01", "Command02"])


@dataclass
class SettingParameters(SettingParametersServer, SettingParametersLocal):
    pass


@dataclass
class GUIParametersLocal:
    pass

@dataclass
class GUIParametersServer:
    window_width: int = 1500
    window_height: int =1000
    font_family = "Meiryo"
    font_size: int = 9
    schedule_font_size: int = 9
    window_bg_color: str = "#9E9E8E"
    schedule_bg_color: str = "#FFF8DC"
    schedule_dy_factor: float = 2.2
    schedule_title_fontsize_factor: float = 1.1


@dataclass
class GUIParameters(GUIParametersServer, GUIParametersLocal):
    pass


class JSONReadWrite:
    def __init__(self, p_dir, user_id, logger):
        self.p_dir = os.path.abspath(p_dir)
        self.local_dir = os.path.dirname(os.path.abspath(p_dir))
        self.user_id = user_id
        self.logger = logger
        self.logger.debug(f"local_dir: {p_dir}")

    def read(self):
        # localに置いている設定データの読み込み
        tmp_local = self._read_json(self.local_dir, f"setting.json")
        assert tmp_local is not None, "setting.json was not FOUND"
        SPL = SettingParametersLocal(**tmp_local["Setting"])
        GPL = GUIParametersLocal(**tmp_local["GUI"])
        # サーバーに置いている設定データの読み込み
        tmp_server = self._read_json(SPL.server_dir, f"setting_{self.user_id}.json")
        if tmp_server is None:
            SPS = SettingParametersServer()
            GPS = GUIParametersServer()
        else:
            SPS = SettingParametersServer(**tmp_server["Setting"])
            GPS = GUIParametersServer(**tmp_server["GUI"])
        SP = SettingParameters(**vars(SPL), **vars(SPS))
        GP = GUIParameters(**vars(GPL), **vars(GPS))

        MEMO = self._read_json(SPL.server_dir, f"memo_{self.user_id}.json")
        if MEMO is None:
            MEMO = self._white_memo()
        INFO = self._read_json(self.p_dir, f"version_report.json", {})
        INFO["Report"] = self._read_json(SPL.server_dir, f"report_{self.user_id}.json", "")

        return SP, GP, MEMO, INFO

    def _read_json(self, p_dir, file_name, return_no_file=None):
        file_name = os.path.join(p_dir, file_name)
        self.logger.debug(f"json file exists: {os.path.exists(file_name)}")
        self.logger.debug(f"read json file: {file_name}")
        if not os.path.exists(file_name):
            return return_no_file
        with open(file_name, encoding="UTF-8") as f:
            tmp = json.load(f)
        return tmp

    def write(self, server_dir, SP=None, GP=None, MEMO=None, BUG_REP=None):
        if SP is not None and GP is not None:
            PL, PS = self._arrange_parameters(SP, GP)
            self._write_json(SP.server_dir, f"setting_{self.user_id}.json", PS)
            self._write_json(self.local_dir, "setting.json", PL)
        if MEMO is not None:
            self._write_json(server_dir, f"memo_{self.user_id}.json", MEMO)
        if BUG_REP is not None:
            self._write_json(server_dir, f"report_{self.user_id}.json", BUG_REP)

    def _write_json(self, p_dir, file_name, save_item):
        file_name = os.path.join(p_dir, file_name)
        self.logger.debug(f"write json file: {file_name}")
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
    user_id = "User"
    p_dir = os.path.dirname(os.path.dirname(__file__))
    json_wr = JSONReadWrite(p_dir, user_id, logger)
    SP, GP, MEMO = json_wr.read()
    print(f"{SP=}")
    print(f"{GP=}")
    print(f"{MEMO=}")

    print()
    json_wr.write(server_dir=SP.server_dir, SP=SP, GP=GP, MEMO=MEMO)