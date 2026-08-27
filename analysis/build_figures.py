#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"


def read_csv(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    FIG.mkdir(exist_ok=True)
    ablation = read_csv("tables/ablation_summary.csv")
    labels = [row["arm"] for row in ablation]
    mae = [float(row["MAE_nm"]) for row in ablation]

    plt.figure(figsize=(7.2, 3.8))
    colors = ["#8c8c8c", "#d8a03d", "#6f9ed6", "#b37ab5", "#5fa37a", "#4269a8"]
    plt.bar(range(len(labels)), mae, color=colors[: len(labels)], edgecolor="#333333", linewidth=0.8)
    plt.ylabel("Mean absolute error (nm)")
    plt.xticks(range(len(labels)), labels, rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(FIG / "stage33_ablation_mae.png", dpi=400)
    plt.savefig(FIG / "stage33_ablation_mae.svg")
    plt.close()

    routing = read_csv("tables/routing_summary.csv")
    values = {row["metric"]: float(row["value"]) for row in routing}
    names = ["A-only improved", "A-only harmed", "Final A+B improved", "Final A+B harmed"]
    counts = [values[name] for name in names]

    plt.figure(figsize=(5.8, 3.6))
    plt.bar(range(len(names)), counts, color=["#6aa57a", "#c86d5a", "#6aa57a", "#c86d5a"], edgecolor="#333333", linewidth=0.8)
    plt.ylabel("Observation count")
    plt.xticks(range(len(names)), names, rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(FIG / "stage33_routing_counts.png", dpi=400)
    plt.savefig(FIG / "stage33_routing_counts.svg")
    plt.close()

    print("wrote figures/stage33_ablation_mae.* and figures/stage33_routing_counts.*")


if __name__ == "__main__":
    main()
