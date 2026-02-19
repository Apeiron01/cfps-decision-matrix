from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def summarize_iqr(series: pd.Series) -> tuple[float, float, float]:
    q1 = series.quantile(0.25)
    q2 = series.quantile(0.5)
    q3 = series.quantile(0.75)
    return q2, q1, q3


def make_boxplot(df: pd.DataFrame, value_col: str, title: str, ylabel: str, outpath: Path) -> None:
    groups = []
    labels = []
    for fmt, sub in df.groupby("format_class"):
        values = sub[value_col].dropna()
        if values.empty:
            continue
        groups.append(values.values)
        labels.append(fmt)

    plt.figure(figsize=(10, 5))
    plt.boxplot(groups, tick_labels=labels, showfliers=False)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outpath, dpi=200)
    plt.savefig(outpath.with_suffix(".tiff"), dpi=300)
    plt.close()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "data_clean" / "cfps_dataset_v1.csv"
    fig_yield = root / "figures" / "yield_by_format.png"
    fig_time = root / "figures" / "time_by_format.png"

    df = pd.read_csv(src)

    # Yield summary
    yield_df = df.dropna(subset=["yield_ug_per_ml"])
    if not yield_df.empty:
        make_boxplot(
            yield_df,
            "yield_ug_per_ml",
            "Yield by format (ug/mL)",
            "yield_ug_per_ml",
            fig_yield,
        )

    # Time summary
    time_df = df.dropna(subset=["time_h"])
    if not time_df.empty:
        make_boxplot(
            time_df,
            "time_h",
            "Reaction time by format (h)",
            "time_h",
            fig_time,
        )

    # Print quick stats
    for label, col in [("yield", "yield_ug_per_ml"), ("time", "time_h")]:
        sub = df.dropna(subset=[col])
        if sub.empty:
            continue
        print(f"summary_{label}:")
        for fmt, grp in sub.groupby("format_class"):
            med, q1, q3 = summarize_iqr(grp[col])
            print(f"  {fmt}: median={med:.2f} IQR=({q1:.2f}, {q3:.2f})")

    print(f"output_figures={fig_yield},{fig_time}")


if __name__ == "__main__":
    main()
