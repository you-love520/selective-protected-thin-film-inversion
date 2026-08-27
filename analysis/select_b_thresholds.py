from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "max_basin_gap_rel",
        "min_local_identifiability",
        "accepted",
        "worsened",
        "overall_mean_delta_ae_nm",
    }
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"grid is empty or missing columns: {sorted(required)}")
    return rows


def select(rows: list[dict], a_only_delta: float, retention: float) -> tuple[dict, int]:
    if not a_only_delta < 0:
        raise ValueError("A-only mean delta must be negative for a benefit-retention rule")
    required_benefit = retention * (-a_only_delta)
    eligible = []
    for row in rows:
        gap_text = row["max_basin_gap_rel"].strip()
        if not gap_text:
            continue
        delta = float(row["overall_mean_delta_ae_nm"])
        benefit = -delta
        if benefit + 1e-15 < required_benefit:
            continue
        parsed = dict(row)
        parsed["max_basin_gap_rel"] = float(gap_text)
        parsed["min_local_identifiability"] = float(row["min_local_identifiability"])
        parsed["accepted"] = int(float(row["accepted"]))
        parsed["worsened"] = int(float(row["worsened"]))
        parsed["overall_mean_delta_ae_nm"] = delta
        eligible.append(parsed)
    if not eligible:
        raise RuntimeError("no grid point satisfies the registered benefit-retention constraint")
    eligible.sort(
        key=lambda row: (
            row["worsened"],
            row["overall_mean_delta_ae_nm"],
            row["accepted"],
            row["max_basin_gap_rel"],
            -row["min_local_identifiability"],
        )
    )
    return eligible[0], len(eligible)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=ROOT / "configs" / "THRESHOLD_SELECTION_INPUT.json")
    parser.add_argument("--output", type=Path, default=ROOT / "analysis" / "THRESHOLD_SELECTION_REPRODUCED_CHECK.json")
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f"refusing to overwrite existing output: {args.output}")
    config = json.loads(args.input.read_text(encoding="utf-8"))
    grid = args.input.parent / config["grid_file"]
    selected, eligible_count = select(
        load_rows(grid),
        float(config["a_only_overall_mean_delta_ae_nm"]),
        float(config["benefit_retention_fraction"]),
    )
    payload = {
        "status": "DETERMINISTIC_REPRODUCTION_PASS",
        "policy": config["selection_policy"],
        "benefit_retention_fraction": config["benefit_retention_fraction"],
        "a_only_overall_mean_delta_ae_nm": config["a_only_overall_mean_delta_ae_nm"],
        "eligible_grid_points": eligible_count,
        "selected": selected,
        "input_sha256": sha256(args.input),
        "grid_sha256": sha256(grid),
    }
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
