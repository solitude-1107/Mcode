from __future__ import annotations

import random
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


SPINNER_VERBS = [
    "实现中", "架构中", "烘焙中", "跳舞中", "迷惑中",
    "吹嘘中", "摇摆中", "瞎搞中", "启动中", "酿造中",
    "计算中", "纠缠中", "焦糖化", "级联中", "思考中",
    "编排中", "搅拌中", "融合中", "沉思中", "整理中",
    "创作中", "计算中", "调制中", "考虑中", "深思中",
    "烹饪中", "制作中", "创建中", "处理中", "结晶中",
    "培育中", "破译中", "审议中", "磨蹭中",
    "混乱中", "涂鸦中", "阐明中", "迷惑中", "构想中",
    "发酵中", "哄骗中", "火焰中", "叽喳中", "困惑中",
    "锻造中", "嬉戏中", "游荡中", "装饰中", "生成中",
    "萌芽中", "律动中", "和谐中", "孵化中", "鸣叫中",
    "喧闹中", "构思中", "想象中", "即兴中", "孵化中",
    "推断中", "注入中", "揉捏中", "闲逛中", "显现中",
    "腌制中", "漫步中", "蜕变中", "喵喵中", "太空步中",
    "溜达中", "琢磨中", "沉思中", "摸索中", "轨道中", "编排中",
    "渗透中", "哲学中", "沉思中", "高谈中", "扑击中",
    "呼噜中", "困惑中", "眼花中", "反刍中", "蹦跳中",
    "炖煮中", "素描中", "探险中", "旋转中", "发芽中",
    "综合中", "思考中", "捣鼓中", "变形中", "转化中",
    "波动中", "展开中", "解开中", "氛围中", "漫步中",
    "搅拌中", "工作中", "争论中", "曲折中",
]


def random_verb() -> str:
    return random.choice(SPINNER_VERBS)


@dataclass
class ToolActivity:
    tool_name: str
    description: str

    @classmethod
    def from_tool_use(cls, tool_name: str, args: dict) -> ToolActivity:
        desc = _describe(tool_name, args)
        return cls(tool_name=tool_name, description=desc)


def _describe(tool_name: str, args: dict) -> str:
    match tool_name:
        case "ReadFile":
            return f"Reading {args.get('file_path', '')}"
        case "EditFile":
            return f"Editing {args.get('file_path', '')}"
        case "WriteFile":
            return f"Writing {args.get('file_path', '')}"
        case "Bash":
            cmd = str(args.get("command", ""))
            return f"Running {cmd[:40]}{'…' if len(cmd) > 40 else ''}"
        case "Glob":
            return f"Searching {args.get('pattern', '')}"
        case "Grep":
            return f"Grepping {args.get('pattern', '')}"
        case _:
            return tool_name


@dataclass
class TeammateProgress:
    name: str
    team_name: str
    status: str = "running"
    tool_use_count: int = 0
    token_count: int = 0
    last_activity: Optional[ToolActivity] = None
    recent_activities: list[ToolActivity] = field(default_factory=list)
    spinner_verb: str = field(default_factory=random_verb)
    start_time: float = field(default_factory=time.monotonic)
    last_message: Optional[str] = None
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record_tool_use(self, tool_name: str, args: dict) -> None:
        with self._lock:
            self.tool_use_count += 1
            act = ToolActivity.from_tool_use(tool_name, args)
            self.last_activity = act
            self.recent_activities.append(act)
            if len(self.recent_activities) > 5:
                self.recent_activities.pop(0)

    def record_tokens(self, input_tokens: int, output_tokens: int) -> None:
        with self._lock:
            self.token_count = input_tokens + output_tokens

    @property
    def activity_summary(self) -> str:
        with self._lock:
            if self.last_activity:
                return self.last_activity.description
            return self.spinner_verb

    @staticmethod
    def format_tokens(n: int) -> str:
        if n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M"
        if n >= 1_000:
            return f"{n / 1_000:.1f}k"
        return str(n)
