#!/usr/bin/env python3
"""コストサマリーを $PETIT_DATA_DIR/cost_summary/<cycle-start>.md に書き出す。

characters/*/stream_logs/*.jsonl (claude --output-format stream-json のログ、
m5-petit-appが書き込むもの)から result イベントの total_cost_usd を集計する。
cron で定期実行して、キャラクターが Bash cat で読めるようにする想定。

使い方:
  python3 generate_cost_summary.py                        # 予算表示なし、暦月区切り
  python3 generate_cost_summary.py --budget 200 --reset-day 26  # 月予算$200、26日締め
"""

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))
DATA_DIR = Path(os.environ.get("PETIT_DATA_DIR", str(Path.home() / "petit_data")))
CHAR_ROOT = DATA_DIR / "characters"
SUMMARY_DIR = DATA_DIR / "cost_summary"


def load_entries():
    """全キャラクターのstream_logsからresultイベントを集める。"""
    entries = []
    if not CHAR_ROOT.is_dir():
        return entries
    for char_dir in CHAR_ROOT.iterdir():
        stream_dir = char_dir / "stream_logs"
        if not stream_dir.is_dir():
            continue
        for jsonl_file in stream_dir.glob("*.jsonl"):
            # ファイル名: YYYYMMDD_HHMMSS_source.jsonl
            parts = jsonl_file.stem.split("_", 2)
            if len(parts) < 3:
                continue
            date_part, time_part, source = parts
            try:
                dt = datetime.strptime(f"{date_part}{time_part}", "%Y%m%d%H%M%S").replace(tzinfo=JST)
            except ValueError:
                continue
            try:
                for line in jsonl_file.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    ev = json.loads(line)
                    if ev.get("type") == "result":
                        entries.append({
                            "date": dt.strftime("%Y-%m-%d"),
                            "character": char_dir.name,
                            "source": source,
                            "cost": ev.get("total_cost_usd", 0) or 0,
                        })
            except Exception:
                continue
    return entries


def calc_cycle(now, reset_day):
    if now.day >= reset_day:
        start = now.replace(day=reset_day, hour=0, minute=0, second=0, microsecond=0)
        nm = now.month + 1 if now.month < 12 else 1
        ny = now.year if now.month < 12 else now.year + 1
        end = now.replace(year=ny, month=nm, day=reset_day, hour=0, minute=0, second=0, microsecond=0)
    else:
        end = now.replace(day=reset_day, hour=0, minute=0, second=0, microsecond=0)
        pm = now.month - 1 if now.month > 1 else 12
        py = now.year if now.month > 1 else now.year - 1
        start = now.replace(year=py, month=pm, day=reset_day, hour=0, minute=0, second=0, microsecond=0)
    return start, end


def main():
    parser = argparse.ArgumentParser(description="Generate a cost summary from stream_logs")
    parser.add_argument("--budget", type=float, default=None, help="月予算(USD)。指定しなければ予算欄は省略")
    parser.add_argument("--reset-day", type=int, default=1, help="サイクルの締め日(1〜28、デフォルト1=暦月)")
    args = parser.parse_args()

    now = datetime.now(JST)
    today_str = now.strftime("%Y-%m-%d")
    entries = load_entries()

    def cost_sum(lst):
        return sum(e.get("cost", 0) for e in lst)

    today_e = [e for e in entries if e.get("date") == today_str]
    today_cost = cost_sum(today_e)

    cycle_start, cycle_end = calc_cycle(now, args.reset_day)
    cs = cycle_start.strftime("%Y-%m-%d")
    ce = cycle_end.strftime("%Y-%m-%d")
    cycle_e = [e for e in entries if cs <= e.get("date", "") < ce]
    cycle_cost = cost_sum(cycle_e)

    by_char = {}
    by_src = {}
    for e in cycle_e:
        c = e.get("character", "unknown")
        s = e.get("source", "unknown")
        by_char[c] = by_char.get(c, 0) + e.get("cost", 0)
        by_src[s] = by_src.get(s, 0) + e.get("cost", 0)

    daily = {}
    cur = cycle_start.date()
    end_date = now.date()
    while cur <= end_date:
        d_str = cur.strftime("%Y-%m-%d")
        day_e = [e for e in entries if e["date"] == d_str]
        daily[d_str] = sum(e["cost"] for e in day_e)
        cur += timedelta(days=1)

    lines = [
        f"# コストサマリー（{now.strftime('%Y-%m-%d %H:%M')} JST 更新）",
        "",
        f"- **今日**: ${today_cost:.3f}",
        f"- **今サイクル合計** ({cs}〜{ce}): ${cycle_cost:.3f}",
    ]
    if args.budget:
        days_elapsed = (now.date() - cycle_start.date()).days
        cycle_days = (cycle_end.date() - cycle_start.date()).days
        ideal = args.budget * days_elapsed / max(cycle_days, 1)
        remaining = max(0, args.budget - cycle_cost)
        days_remaining = (cycle_end.date() - now.date()).days
        lines += [
            f"- **理想値** (今日まで): ${ideal:.2f}",
            f"- **残り予算**: ${remaining:.2f}（残り{days_remaining}日）",
            f"- **予算上限**: ${args.budget:.0f}",
        ]
    lines += ["", "## キャラクター別（今サイクル）"]
    for char, cost in sorted(by_char.items(), key=lambda x: -x[1]):
        lines.append(f"- {char}: ${cost:.3f}")

    lines += ["", "## ソース別（今サイクル）"]
    src_labels = {"chat": "チャット", "sensor": "センサー", "camera": "カメラ", "mic": "マイク", "diary": "日記", "terminal_chat": "ターミナルチャット"}
    for src, cost in sorted(by_src.items(), key=lambda x: -x[1]):
        label = src_labels.get(src, src)
        lines.append(f"- {label}: ${cost:.3f}")

    lines += ["", "## 日別（今サイクル）"]
    for d_str, cost in sorted(daily.items()):
        marker = " ← 今日" if d_str == today_str else ""
        lines.append(f"- {d_str}: ${cost:.3f}{marker}")

    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    out_file = SUMMARY_DIR / f"{cs}.md"
    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"written: {out_file}")


if __name__ == "__main__":
    main()
