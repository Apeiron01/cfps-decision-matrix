from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCENARIOS = {
    "Speed-first": {
        "time_score": 0.40,
        "yield_score": 0.20,
        "complexity_score": 0.15,
        "scalability_score": 0.10,
        "automation_score": 0.15,
    },
    "Yield-first": {
        "yield_score": 0.45,
        "time_score": 0.15,
        "complexity_score": 0.10,
        "scalability_score": 0.15,
        "automation_score": 0.15,
    },
    "Low-infra-first": {
        "complexity_score": 0.40,
        "time_score": 0.20,
        "yield_score": 0.15,
        "scalability_score": 0.10,
        "automation_score": 0.15,
    },
}


def minmax(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    min_v = s.min()
    max_v = s.max()
    if np.isclose(min_v, max_v):
        return pd.Series([0.5] * len(s), index=s.index)
    return (s - min_v) / (max_v - min_v)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_path = root / "data_clean" / "cfps_dataset_v1.csv"
    taxonomy_path = root / "protocol" / "taxonomy.csv"
    out_csv = root / "data_clean" / "mcda_scores_v1.csv"
    fig_path = root / "figures" / "decision_matrix_heatmap.png"

    df = pd.read_csv(data_path)
    taxonomy = pd.read_csv(taxonomy_path)

    observed_formats = set(df["format_class"].dropna().unique())
    taxonomy = taxonomy[taxonomy["format_class"].isin(observed_formats)].copy()

    agg = df.groupby("format_class").agg(
        yield_median=("yield_ug_per_ml", "median"),
        time_median=("time_h", "median"),
    )

    base = taxonomy[[
        "format_class",
        "complexity_proxy",
        "scalability_proxy",
        "automation_proxy",
    ]].merge(agg, on="format_class", how="left")

    if base["yield_median"].isna().all():
        base["yield_median"] = 0.0
    else:
        base["yield_median"] = base["yield_median"].fillna(base["yield_median"].median())

    if base["time_median"].isna().all():
        base["time_median"] = 0.0
    else:
        base["time_median"] = base["time_median"].fillna(base["time_median"].median())

    yield_score = minmax(base["yield_median"])
    time_score = 1.0 - minmax(base["time_median"])
    complexity_score = 1.0 - minmax(base["complexity_proxy"])
    scalability_score = minmax(base["scalability_proxy"])
    automation_score = minmax(base["automation_proxy"])

    score_table = pd.DataFrame({
        "format_class": base["format_class"],
        "yield_score": yield_score,
        "time_score": time_score,
        "complexity_score": complexity_score,
        "scalability_score": scalability_score,
        "automation_score": automation_score,
    })

    rows = []
    for scenario, weights in SCENARIOS.items():
        for _, r in score_table.iterrows():
            components = {
                "yield_score": float(r["yield_score"]),
                "time_score": float(r["time_score"]),
                "complexity_score": float(r["complexity_score"]),
                "scalability_score": float(r["scalability_score"]),
                "automation_score": float(r["automation_score"]),
            }
            total = 0.0
            for key, w in weights.items():
                total += components[key] * w
            rows.append({
                "format_class": r["format_class"],
                "scenario": scenario,
                "total_score": round(total, 6),
                "component_scores_json": json.dumps(components),
            })

    out = pd.DataFrame(rows)
    out.to_csv(out_csv, index=False)

    # Heatmap
    pivot = out.pivot(index="format_class", columns="scenario", values="total_score")
    plt.figure(figsize=(8, 5))
    plt.imshow(pivot.values, aspect="auto", cmap="viridis")
    plt.colorbar(label="total_score")
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=20, ha="right")
    plt.title("Decision matrix scores")
    plt.tight_layout()
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(fig_path, dpi=200)
    plt.savefig(fig_path.with_suffix(".tiff"), dpi=300)
    plt.close()

    print(f"output_csv={out_csv}")
    print(f"output_figure={fig_path}")


if __name__ == "__main__":
    main()
