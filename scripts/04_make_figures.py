from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def make_heatmap(df: pd.DataFrame, outpath: Path) -> None:
    pivot = df.pivot(index="format_class", columns="scenario", values="total_score")
    plt.figure(figsize=(8, 5))
    plt.imshow(pivot.values, aspect="auto", cmap="viridis")
    plt.colorbar(label="total_score")
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=20, ha="right")
    plt.title("Decision matrix scores")
    plt.tight_layout()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outpath, dpi=200)
    plt.savefig(outpath.with_suffix(".tiff"), dpi=300)
    plt.close()


def make_radar(df: pd.DataFrame, outpath: Path) -> None:
    components = [
        "yield_score",
        "time_score",
        "complexity_score",
        "scalability_score",
        "automation_score",
    ]
    labels = ["Yield", "Time", "Complexity", "Scalability", "Automation"]

    records = []
    for _, row in df.iterrows():
        comp = json.loads(row["component_scores_json"])
        rec = {"scenario": row["scenario"]}
        for c in components:
            rec[c] = comp.get(c, np.nan)
        records.append(rec)

    comp_df = pd.DataFrame(records)
    mean_df = comp_df.groupby("scenario")[components].mean()

    angles = np.linspace(0, 2 * np.pi, len(components), endpoint=False)
    angles = np.concatenate([angles, angles[:1]])

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)

    for scenario, row in mean_df.iterrows():
        values = row.values.astype(float)
        values = np.concatenate([values, values[:1]])
        ax.plot(angles, values, linewidth=2, label=scenario)
        ax.fill(angles, values, alpha=0.1)

    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_ylim(0, 1)
    ax.set_title("Average component scores by scenario")
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
    plt.tight_layout()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outpath, dpi=200)
    plt.savefig(outpath.with_suffix(".tiff"), dpi=300)
    plt.close()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "data_clean" / "mcda_scores_v1.csv"
    heatmap = root / "figures" / "decision_matrix_heatmap.png"
    radar = root / "figures" / "radar_by_scenario.png"

    df = pd.read_csv(src)
    make_heatmap(df, heatmap)
    make_radar(df, radar)

    print(f"output_figure={heatmap}")
    print(f"output_figure={radar}")


if __name__ == "__main__":
    main()
