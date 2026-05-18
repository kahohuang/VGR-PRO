from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


STATUS_INITIAL = "初步建联中"
STATUS_REPLIED = "初次建联已回复"
STATUS_SECOND_TOUCH = "二次建联"
STATUS_SECOND_TALKING = "二次建联沟通中"
STATUS_COOPERATING = "达成合作"
STATUS_SAMPLE_SENT = "寄样"
STATUS_SAMPLE_DELIVERED = "样品已送达"
STATUS_VIDEO_POSTED = "视频已发布"
STATUS_LOST = "失联达人"
STATUS_OVERDUE = "逾期达人"


@dataclass
class CreatorRecord:
    date: datetime | date | None
    username: str
    product: str | None
    whatsapp_status: str | None
    whatsapp_contact: str | None
    posted_video_count: int | float | str | None
    tk_profile_url: str | None
    cooperation_status: str | None
    owner: str | None
    authorization_status: str | None
    fathers_day_status: str | None
    notes: str | None
