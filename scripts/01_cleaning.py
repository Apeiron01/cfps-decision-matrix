from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def normalize_yield(row: pd.Series) -> tuple[float | None, str, bool, bool]:
    value = row.get("yield_value")
    unit = str(row.get("yield_unit") or "").strip()
    notes = str(row.get("notes") or "").strip()

    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None, notes, False, False

    unit = unit.replace("\u00b5", "u").replace("\u03bc", "u")
    unit_lc = unit.lower().replace(" ", "")

    if unit_lc in {"ug/ml", "ugperml", "ug/ml."}:
        return float(value), notes, False, False
    if unit_lc in {"mg/ml", "mgpermL", "mgperml", "mg/ml."}:
        return float(value) * 1000.0, notes, True, False
    if "um" in unit_lc:
        msg = "not convertible (molar unit)"
        notes = f"{notes}; {msg}".strip("; ")
        return None, notes, False, True

    msg = f"not convertible (unit={unit})"
    notes = f"{notes}; {msg}".strip("; ")
    return None, notes, False, True


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src_xlsx = root / "data_raw" / "extraction_template.xlsx"
    src_csv = root / "data_raw" / "extraction_template.csv"
    fallback = root / "data_raw" / "extraction_dummy.xlsx"
    dst = root / "data_clean" / "cfps_dataset_v1.csv"

    df = None
    if src_xlsx.exists():
        try:
            df_xlsx = pd.read_excel(src_xlsx, sheet_name="extraction", engine="openpyxl")
            if len(df_xlsx) > 0:
                df = df_xlsx
        except Exception:
            df = None

    if df is None and src_csv.exists():
        df_csv = pd.read_csv(src_csv)
        if len(df_csv) > 0:
            df = df_csv

    if df is None:
        df = pd.read_excel(fallback, sheet_name="extraction", engine="openpyxl")

    converted = 0
    not_convertible = 0
    yield_ug_per_ml = []
    notes_out = []

    for _, row in df.iterrows():
        y, notes, was_converted, was_not_convertible = normalize_yield(row)
        if was_converted:
            converted += 1
        if was_not_convertible:
            not_convertible += 1
        yield_ug_per_ml.append(y)
        notes_out.append(notes)

    df["yield_ug_per_ml"] = yield_ug_per_ml
    df["notes"] = notes_out

    df.to_csv(dst, index=False)

    total = len(df)
    print(f"rows_read={total}")
    print(f"converted_units={converted}")
    print(f"not_convertible={not_convertible}")
    print(f"output={dst}")


if __name__ == "__main__":
    main()
