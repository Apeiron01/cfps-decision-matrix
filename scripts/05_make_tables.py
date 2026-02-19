from __future__ import annotations

from pathlib import Path
import json
import pandas as pd


def write_markdown_table(df: pd.DataFrame, md_path: Path) -> None:
    headers = list(df.columns)
    md_lines = []
    md_lines.append("| " + " | ".join(headers) + " |\n")
    md_lines.append("|" + "|".join(["---"] * len(headers)) + "|\n")
    for _, row in df.iterrows():
        values = [str(row[h]) for h in headers]
        md_lines.append("| " + " | ".join(values) + " |\n")
    md_path.write_text("".join(md_lines), encoding="ascii")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out_dir = root / "output"
    out_dir.mkdir(exist_ok=True)

    # Table 1: Study-level summary
    cfps = pd.read_csv(root / "data_clean" / "cfps_dataset_v1.csv")
    table1 = cfps[["paper_id", "format_class", "yield_value", "yield_unit", "time_h", "lysate_type"]].copy()
    t1_csv = out_dir / "table1_cfps_results.csv"
    t1_md = out_dir / "table1_cfps_results.md"
    table1.to_csv(t1_csv, index=False)
    write_markdown_table(table1, t1_md)

    # Table 2: MCDA weights
    weights = {
        "Speed-first": {
            "time": 0.40,
            "yield": 0.20,
            "complexity": 0.15,
            "scalability": 0.10,
            "automation": 0.15,
        },
        "Yield-first": {
            "yield": 0.45,
            "time": 0.15,
            "complexity": 0.10,
            "scalability": 0.15,
            "automation": 0.15,
        },
        "Low-infra-first": {
            "complexity": 0.40,
            "time": 0.20,
            "yield": 0.15,
            "scalability": 0.10,
            "automation": 0.15,
        },
    }
    rows = []
    for scenario, w in weights.items():
        rows.append({
            "scenario": scenario,
            "yield": w["yield"],
            "time": w["time"],
            "complexity": w["complexity"],
            "scalability": w["scalability"],
            "automation": w["automation"],
        })
    table2 = pd.DataFrame(rows)
    t2_csv = out_dir / "table2_mcda_weights.csv"
    t2_md = out_dir / "table2_mcda_weights.md"
    table2.to_csv(t2_csv, index=False)
    write_markdown_table(table2, t2_md)

    # Table 3: MCDA scores (pivot)
    mcda = pd.read_csv(root / "data_clean" / "mcda_scores_v1.csv")
    pivot = mcda.pivot(index="format_class", columns="scenario", values="total_score").reset_index()
    pivot.columns.name = None
    table3 = pivot
    t3_csv = out_dir / "table3_mcda_scores.csv"
    t3_md = out_dir / "table3_mcda_scores.md"
    table3.to_csv(t3_csv, index=False)
    write_markdown_table(table3, t3_md)

    # Table 4: Taxonomy proxies
    taxonomy = pd.read_csv(root / "protocol" / "taxonomy.csv")
    table4 = taxonomy[[
        "format_class",
        "complexity_proxy",
        "scalability_proxy",
        "automation_proxy",
    ]].copy()
    t4_csv = out_dir / "table4_taxonomy_proxies.csv"
    t4_md = out_dir / "table4_taxonomy_proxies.md"
    table4.to_csv(t4_csv, index=False)
    write_markdown_table(table4, t4_md)

    print("wrote", t1_csv)
    print("wrote", t1_md)
    print("wrote", t2_csv)
    print("wrote", t2_md)
    print("wrote", t3_csv)
    print("wrote", t3_md)
    print("wrote", t4_csv)
    print("wrote", t4_md)


if __name__ == "__main__":
    main()
