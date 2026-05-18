from __future__ import annotations

from typing import Any


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def generate_english_message(intent_cn: str, creator_context: dict[str, Any]) -> str:
    text = clean_text(intent_cn)
    lowered = text.lower()
    repeat_creator = bool(creator_context.get("is_repeat_creator"))
    fathers_day = bool(creator_context.get("is_fathers_day"))
    has_wsp = bool(creator_context.get("has_whatsapp"))
    stage = clean_text(creator_context.get("stage"))

    wants_soft = any(keyword in text for keyword in ("轻一点", "别太硬", "别太急", "客气", "自然"))
    mention_review = "审核" in text
    mention_traffic = "流量" in text or "support" in lowered
    mention_next_week = "下周" in text
    mention_schedule = "排期" in text or "时间" in text or "timeline" in lowered

    if "ad code" in lowered or "授权" in text or stage == "待获取ad code":
        opening = "Hey bro, I saw the video is live."
        ask = "When you get a chance, could you send me the ad code for this video?"
        close = (
            "Once I have it, I can start putting traffic behind it right away."
            if mention_traffic or not wants_soft
            else "Once I have it, I can start supporting the video on my side."
        )
        return f"{opening} {ask} {close}"

    if "账号授权" in text:
        return (
            "Hey bro, thanks again for posting the video. If you're open to it, I'd also love to set up account authorization "
            "so we can keep scaling the content more smoothly on our side."
        )

    if "申请样品" in text or stage == "待申请样品":
        tone = "Whenever you have a moment," if wants_soft else "Please"
        review = " I'll review it as soon as it comes through." if mention_review or wants_soft else " I'll approve it as soon as I see it."
        traffic = " Once the sample is approved, I'll also line up traffic support for the video." if mention_traffic else ""
        return (
            f"Hey bro, just following up on the sample application for the VGR PRO 886. {tone} submit the free sample request in TikTok Shop and"
            f"{review}{traffic}"
        )

    if "收货" in text or "收到" in text or stage == "已寄样待确认收货":
        return (
            "Hey bro, just checking in to see whether the sample has arrived yet. "
            "If you've received it, let me know and I'll help line up the next steps on my side."
        )

    if "发布" in text or "视频" in text or stage in {"已收货待发布", "老达人复合作"}:
        if repeat_creator:
            next_week = " next week" if mention_next_week else ""
            schedule = (
                " If you already have a timeline in mind, let me know and I'll coordinate support on my side."
                if mention_schedule or mention_traffic
                else ""
            )
            festival = " This Father's Day window could also be a strong angle for the content." if fathers_day else ""
            return f"Hey bro, I just wanted to check whether you might be able to post the new video{next_week}.{schedule}{festival}"
        tone = "when you have a moment" if wants_soft else "as soon as you can"
        traffic = " Once the video is live, I'll push traffic support behind it on my side." if mention_traffic or has_wsp else ""
        return (
            f"Hey bro, just wanted to follow up on the video. If you've already received the sample, please try to post it {tone}."
            f"{traffic}"
        )

    if "whatsapp" in lowered or "加" in text and "WhatsApp" in text:
        return (
            "Hey bro, it might be easier to confirm the details on WhatsApp. "
            "If you're okay with it, please send me your WhatsApp number and I'll message you there."
        )

    if "合作" in text or stage in {"WhatsApp沟通中", "已加WhatsApp待推进", "WhatsApp已接通"}:
        return (
            "Hey bro, just checking in on the collaboration. "
            "If you're still interested, let me know your timeline and I can help move everything forward on my side."
        )

    return (
        "Hey bro, just following up here. "
        "Let me know when you get a chance, and I'll keep everything moving on my side."
    )
