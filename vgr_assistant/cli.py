from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .analysis import analyze_records, load_creator_records
from .messaging import generate_english_message
from .reporting import render_markdown_report, write_csv, write_dashboard_html


def find_default_workbook(base_dir: Path) -> Path:
    matches = list(base_dir.rglob("涓汉杈句汉寤鸿仈琛?xlsx"))
    if not matches:
        raise FileNotFoundError("鏈壘鍒?涓汉杈句汉寤鸿仈琛?xlsx")
    return matches[0]


def analyze_workbook(workbook_path: Path, output_dir: Path) -> tuple[Path, Path, Path]:
    records = load_creator_records(workbook_path)
    results = analyze_records(records)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_date = date.today()
    csv_path = output_dir / f"vgr_followup_{report_date.isoformat()}.csv"
    md_path = output_dir / f"vgr_followup_{report_date.isoformat()}.md"
    dashboard_path = output_dir / "vgr_dashboard.html"
    write_csv(results, csv_path)
    md_path.write_text(render_markdown_report(results, report_date), encoding="utf-8-sig")
    write_dashboard_html(results, dashboard_path, report_date)
    return csv_path, md_path, dashboard_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VGR PRO 杈句汉璺熻繘涓庤嫳鏂囨秷鎭姪鎵?")
    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser("analyze", help="鍒嗘瀽杈句汉琛ㄥ苟鐢熸垚浠婃棩寰呭姙")
    analyze_parser.add_argument("--workbook", type=Path, default=None, help="杈句汉寤鸿仈琛ㄨ矾寰?")
    analyze_parser.add_argument("--output-dir", type=Path, default=Path("outputs"), help="杈撳嚭鐩綍")

    message_parser = subparsers.add_parser("message", help="鎶婁腑鏂囨剰鍥炬敼鍐欐垚鍙彂閫佽嫳鏂?")
    message_parser.add_argument("--intent", required=True, help="涓枃杩愯惀鎰忓浘")
    message_parser.add_argument("--stage", default="", help="杈句汉褰撳墠闃舵")
    message_parser.add_argument("--repeat", action="store_true", help="鏄惁鑰佽揪浜?")
    message_parser.add_argument("--whatsapp", action="store_true", help="鏄惁宸插姞 WhatsApp")
    message_parser.add_argument("--fathers-day", action="store_true", help="鏄惁鐖朵翰鑺備笓椤?")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "message":
        print(
            generate_english_message(
                args.intent,
                {
                    "is_repeat_creator": args.repeat,
                    "has_whatsapp": args.whatsapp,
                    "is_fathers_day": args.fathers_day,
                    "stage": args.stage,
                },
            )
        )
        return

    base_dir = Path(__file__).resolve().parent.parent
    workbook_path = args.workbook if getattr(args, "workbook", None) else find_default_workbook(base_dir)
    csv_path, md_path, dashboard_path = analyze_workbook(workbook_path, args.output_dir)
    print(f"CSV report: {csv_path}")
    print(f"Markdown report: {md_path}")
    print(f"Dashboard: {dashboard_path}")
