#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tables" / "stage33_public_summary.csv"


def read_csv(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    ablation = {row["arm"]: row for row in read_csv("tables/ablation_summary.csv")}
    routing = {row["metric"]: row["value"] for row in read_csv("tables/routing_summary.csv")}
    summary = [
        {"metric": "n_observations", "value": "7200"},
        {"metric": "E3_MAE_nm", "value": f"{float(ablation['E3']['MAE_nm']):.12f}"},
        {"metric": "Final_AB_MAE_nm", "value": f"{float(ablation['Final A+B']['MAE_nm']):.12f}"},
        {"metric": "A_only_accepted", "value": str(int(float(routing["A-only accepted"])))},
        {"metric": "A_only_improved", "value": str(int(float(routing["A-only improved"])))},
        {"metric": "A_only_harmed", "value": str(int(float(routing["A-only harmed"])))},
        {"metric": "Final_AB_accepted", "value": str(int(float(routing["Final A+B accepted"])))},
        {"metric": "Final_AB_improved", "value": str(int(float(routing["Final A+B improved"])))},
        {"metric": "Final_AB_harmed", "value": str(int(float(routing["Final A+B harmed"])))},
        {"metric": "Final_AB_fallback", "value": str(int(float(ablation["Final A+B"]["fallback"])))},
    ]
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary)
    print(f"wrote {OUT.relative_to(ROOT)} from manuscript-aligned summary tables")


if __name__ == "__main__":
    main()
