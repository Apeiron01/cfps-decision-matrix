from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    counts_path = root / "protocol" / "prisma_counts.csv"
    fig_path = root / "figures" / "prisma_flow.png"

    counts = pd.read_csv(counts_path).set_index("stage")["count"].to_dict()

    # Extract counts
    records_identified = counts.get("records_identified", 0)
    duplicates_removed = counts.get("duplicates_removed", 0)
    records_screened = counts.get("records_screened", 0)
    records_excluded = counts.get("records_excluded", 0)
    full_text_assessed = counts.get("full_text_assessed", 0)
    full_text_excluded = counts.get("full_text_excluded", 0)
    studies_included = counts.get("studies_included", 0)

    # Layout
    plt.figure(figsize=(7, 6))
    ax = plt.gca()
    ax.axis("off")

    boxes = [
        (0.1, 0.85, 0.8, 0.1, f"Records identified (n={records_identified})"),
        (0.1, 0.72, 0.8, 0.1, f"Duplicates removed (n={duplicates_removed})"),
        (0.1, 0.59, 0.8, 0.1, f"Records screened (n={records_screened})"),
        (0.1, 0.46, 0.8, 0.1, f"Records excluded (n={records_excluded})"),
        (0.1, 0.33, 0.8, 0.1, f"Full-text assessed (n={full_text_assessed})"),
        (0.1, 0.20, 0.8, 0.1, f"Full-text excluded (n={full_text_excluded})"),
        (0.1, 0.07, 0.8, 0.1, f"Studies included (n={studies_included})"),
    ]

    for (x, y, w, h, text) in boxes:
        rect = plt.Rectangle((x, y), w, h, fill=False, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10)

    # Arrows
    for i in range(len(boxes) - 1):
        x, y, w, h, _ = boxes[i]
        x2, y2, w2, h2, _ = boxes[i + 1]
        ax.annotate(
            "",
            xy=(x2 + w2 / 2, y2 + h2),
            xytext=(x + w / 2, y),
            arrowprops=dict(arrowstyle="-|>", lw=1.0),
        )

    plt.title("PRISMA Flow Diagram")
    plt.tight_layout()
    fig_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(fig_path, dpi=200)
    plt.close()

    print("wrote", fig_path)


if __name__ == "__main__":
    main()
