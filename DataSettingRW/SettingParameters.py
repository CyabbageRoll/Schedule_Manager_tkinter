from dataclasses import dataclass, asdict, field
from typing import List


@dataclass
class SettingParameters:
    user: str = "Member01"
    members: List[str] = field(default_factory=lambda: ["Member02", "Member03", "Member04", "Member05"])


@dataclass
class GUIParameters:
    window_width: int = 1200
    window_height: int = 900
    window_bg_color: str = "#808080"


