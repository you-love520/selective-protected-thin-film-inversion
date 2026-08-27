#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS {message}")


def close(actual: float, expected: float, tol: float = 5e-9) -> bool:
    return math.isclose(actual, expected, rel_tol=0.0, abs_tol=tol)


def keyed(rows: list[dict[str, str]], key: str, value: str) -> dict[str, float]:
    return {row[key]: float(row[value]) for row in rows}


def main() -> None:
    params = read_json("configs/final_ab_parameters.json")
    protected = read_json("configs/protected_refinement_parameters.json")
    selected = read_json("configs/THRESHOLD_SELECTION_REPRODUCED.json")["selected"]
    ablation = {row["arm"]: row for row in read_csv("tables/ablation_summary.csv")}
    routing = keyed(read_csv("tables/routing_summary.csv"), "metric", "value")
    scenarios = {row["scenario"]: row for row in read_csv("tables/scenario_routing_summary.csv")}
    c2 = {row["group"]: row for row in read_csv("tables/c2_summary.csv")}
    public = keyed(read_csv("tables/stage33_public_summary.csv"), "metric", "value")

    require(params["development"]["master_seed"] == 20260426, "development seed is 20260426")
    require(params["independent_validation"]["master_seed"] == 20260508, "validation seed is 20260508")
    require("7200 observations" in params["independent_validation"]["design"], "validation design contains 7200 observations")
    require(params["adaptive_protection"]["eta2"] == "C2", "adaptive protection uses eta2 = C2")
    require(protected["physical_projection"]["adaptive_eta_rule"] == "eta2 = C2", "source configuration uses eta2 = C2")
    require(close(float(selected["max_basin_gap_rel"]), 5.0), "selected basin-gap threshold is 5.0")
    require(close(float(selected["min_local_identifiability"]), 0.82), "selected local-identifiability threshold is 0.82")
    require(close(float(protected["diagnostic_routing"]["max_basin_gap_rel"]), 5.0), "routing configuration uses basin-gap threshold 5.0")
    require(close(float(protected["diagnostic_routing"]["min_local_identifiability"]), 0.82), "routing configuration uses local-identifiability threshold 0.82")

    expected_mae = {
        "E3": 0.2234648283461462,
        "A + adaptive C2": 0.21660082834614622,
        "Final A+B": 0.19463382834614618,
    }
    for arm, expected in expected_mae.items():
        require(close(float(ablation[arm]["MAE_nm"]), expected), f"{arm} manuscript MAE is fixed")

    expected_counts = {
        "A-only accepted": 2976,
        "A-only improved": 2053,
        "A-only harmed": 923,
        "Final A+B accepted": 2410,
        "Final A+B improved": 1915,
        "Final A+B harmed": 495,
    }
    for metric, expected in expected_counts.items():
        require(int(routing[metric]) == expected, f"{metric} equals {expected}")
    require(int(ablation["Final A+B"]["fallback"]) == 4790, "exact-anchor fallback equals 4790")
    require(close(routing["Harmful rejection rate"], 0.4637053087757313), "harmful rejection rate matches manuscript table")
    require(close(routing["Beneficial retention rate"], 0.9327812956648807), "beneficial retention rate matches manuscript table")
    require(close(routing["Global mean(A+B-A-only)"], -0.021967), "A+B minus A-only mean contrast matches manuscript table")
    require(close(routing["Global mean(A+B-E3)"], -0.028831), "A+B minus E3 mean contrast matches manuscript table")

    expected_scenarios = {
        "Gaussian": (526, 395, 131, 1274),
        "Impulsive": (414, 346, 68, 1386),
        "Baseline drift": (825, 696, 129, 975),
        "Mixed": (645, 478, 167, 1155),
    }
    for name, expected in expected_scenarios.items():
        row = scenarios[name]
        actual = tuple(int(row[column]) for column in ("AB_accepted", "AB_improved", "AB_harmed", "AB_fallback"))
        require(actual == expected, f"{name} routing summary matches manuscript")
        require(int(row["n"]) == 1800, f"{name} contains 1800 summarized observations")

    require(int(c2["inactive"]["n"]) == 2400, "C2 inactive group contains 2400 observations")
    require(int(c2["C2<0.90"]["n"]) == 1456, "low-C2 group contains 1456 observations")
    require(int(c2["C2>=0.90"]["n"]) == 3344, "high-C2 group contains 3344 observations")
    require(int(c2["overall"]["n"]) == 7200, "C2 summary contains 7200 observations")

    require(int(public["n_observations"]) == 7200, "public summary reports 7200 observations")
    require(close(public["Final_AB_MAE_nm"], float(ablation["Final A+B"]["MAE_nm"])), "public summary Final A+B MAE matches ablation table")
    require(int(public["Final_AB_fallback"]) == int(ablation["Final A+B"]["fallback"]), "public summary fallback matches ablation table")

    print("\nSTAGE33 PUBLIC SUMMARY VERIFICATION PASS")


if __name__ == "__main__":
    main()
