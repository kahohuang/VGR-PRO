from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Any

from .dashboard import render_dashboard_html


def render_markdown_report(results: list[dict[str, Any]], report_date: date) -> str:
    lines = [
        f"# VGR PRO Follow-Up Report - {report_date.isoformat()}",
        "",
        f"Total creators: {len(results)}",
        f"High priority: {sum(1 for item in results if item['priority'] == '楂?')}",
        f"Medium priority: {sum(1 for item in results if item['priority'] == '涓?')}",
        "",
        "| Username | Stage | Priority | Blocker | Next Action | Repeat Creator | Needs Sample | English Message |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in results[:150]:
        lines.append(
            "| {username} | {stage} | {priority} | {blocker} | {next_action} | {is_repeat_creator} | {needs_sample} | {english_message} |".format(
                **item
            )
        )
    return "\n".join(lines) + "\n"


def write_csv(results: list[dict[str, Any]], output_path: Path) -> None:
    fieldnames = [
        "date",
        "username",
        "product",
        "has_whatsapp",
        "whatsapp_status",
        "whatsapp_contact",
        "posted_video_count",
        "tk_profile_url",
        "cooperation_status",
        "owner",
        "authorization_raw",
        "authorization_type",
        "fathers_day_status",
        "is_fathers_day",
        "notes",
        "is_repeat_creator",
        "needs_sample",
        "stage",
        "stalled_days",
        "blocker",
        "next_action",
        "priority",
        "english_message",
    ]
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def write_dashboard_html(results: list[dict[str, Any]], output_path: Path, report_date: date) -> None:
    output_path.write_text(render_dashboard_html(results, report_date), encoding="utf-8")
