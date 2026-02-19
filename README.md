# CFPS Decision Matrix (Plan A)

This repo builds a reproducible pipeline for a literature-only CFPS/CFE reactor format decision matrix. It includes protocol files, extraction templates, cleaning/analysis/MCDA scripts, and figure outputs. The first iteration runs end-to-end on a dummy dataset to validate the workflow.

Why This Matter
CFPS reactor formats are diverse and rapidly evolving, yet researchers lack a standardized, goal-oriented framework to decide which format best fits a given application.

## Decision criteria (MCDA)
- Yield (normalized, higher is better)
- Time-to-result (inverse normalized)
- Technical complexity (proxy from taxonomy)
- Scalability (proxy)
- Automation compatibility (proxy)

## Setup (Windows)
Run in the repo root:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install pandas numpy matplotlib scipy statsmodels scikit-learn openpyxl pyarrow
pip freeze > requirements.txt
```

## Run the pipeline
Each step is a single command from repo root:

```powershell
python scripts/00_env_check.py
python scripts/01_cleaning.py
python scripts/02_analysis.py
python scripts/03_mcda.py
python scripts/04_make_figures.py
python scripts/05_make_tables.py
python scripts/06_prisma_flow.py
```

## Outputs
- `data_raw/extraction_template.xlsx`: blank template for real extraction
- `data_raw/extraction_dummy.xlsx`: dummy dataset used for the first run
- `data_clean/cfps_dataset_v1.csv`: cleaned dataset with normalized `yield_ug_per_ml`
- `data_clean/mcda_scores_v1.csv`: MCDA scores per format and scenario
- `figures/yield_by_format.png` and `.tiff`: yield distribution by format (TIFF at 300 dpi)
- `figures/time_by_format.png` and `.tiff`: time distribution by format (TIFF at 300 dpi)
- `figures/decision_matrix_heatmap.png` and `.tiff`: heatmap of scenario scores (TIFF at 300 dpi)
- `figures/radar_by_scenario.png` and `.tiff`: radar comparison per scenario (TIFF at 300 dpi)
- `figures/prisma_flow.png`: PRISMA flow diagram
- `output/table1_cfps_results.csv`: study-level summary table (CSV)
- `output/table1_cfps_results.md`: study-level summary table (Markdown)
- `output/table2_mcda_weights.csv`: MCDA weights (CSV)
- `output/table2_mcda_weights.md`: MCDA weights (Markdown)
- `output/table3_mcda_scores.csv`: MCDA scores by scenario and format (CSV)
- `output/table3_mcda_scores.md`: MCDA scores by scenario and format (Markdown)
- `output/table4_taxonomy_proxies.csv`: taxonomy proxy scores (CSV)
- `output/table4_taxonomy_proxies.md`: taxonomy proxy scores (Markdown)

## Transition to real literature extraction
1. Copy `data_raw/extraction_template.xlsx` and fill with real records.
2. Required fields for inclusion:
   - `paper_id` (or `doi`)
   - `format_class` and/or `format_detail`
   - `yield_value` + `yield_unit`
   - `time_h`
   - `lysate_type`
3. Keep `yield_unit` consistent where possible (prefer `ug/mL`).
4. Re-run the pipeline commands above to regenerate the cleaned dataset, figures, and MCDA scores.

## Protocol and PRISMA
See `protocol/` for scope, taxonomy, search strings, inclusion/exclusion criteria, and PRISMA screening log fields.

## Codex prompts for extraction QA (optional)
Use these prompts in Copilot Chat / Codex alongside `data_raw/extraction_template.xlsx` to validate records.

### 1) Extraction QA + screening assistant
```
Sen bir akademik extraction ve kalite kontrol agentsin. Kullanici, CFPS (Cell-Free Protein Synthesis) reaktor formatlari uzerine sistematik bir literatur analizi yapiyor. Extraction_template.xlsx dosyasina literaturden veri isliyor.

Amaci:
- Farkli reaktor formatlarini (batch, microfluidic, CECF, etc.)
- Verim (yield), sure (time), altyapi uyumu gibi kriterlerle karsilastirmak
- Cok birimli (multi-criteria) karar matrisi uretmek

Senin gorevin:
1. Kullanicinin verdigi her satir icin sunlari kontrol et:
   - Zorunlu alanlar dolu mu? (paper_id, format_class, yield_value, yield_unit, time_h, lysate_type)
   - yield_unit uyumlu mu? (ug/mL ve micro yazim varyantlari normalize edilebilir mi?)
   - format_class mantikli atanmis mi? (ornegin: droplet-based -> microfluidic)
   - Belirsiz veya tahmine dayali veri var mi? (varsa -> notes kismina uyari ekle)

2. Eger veri cikarilamaz durumdaysa aciklayici uyari yaz:
   - "Only fold-change reported"
   - "No absolute yield/time value"

3. Her kayit icin QA sonucu su sekilde ozetle:
   - ✅ Extraction valid
   - ⚠️ Minor issue: unit ambiguity
   - ❌ Invalid: missing core metrics

Unutma: Kullanici veriye dayanmayan tahminde bulunmayacak. Senin gorevin, her kaydin guvenilirligini olcmek ve extraction kalitesini guvence altina almak.
```

### 2) Literature search string helper
```
Sen bilimsel tarama danismanisin. Konu: Cell-Free Protein Synthesis (CFPS) reaktor formatlari.

Amacim:
- Farkli reaktor formatlarini (batch, microfluidic, CECF vs.) hiz, verim, maliyet, altyapi gibi kriterlerle kiyaslayan literaturu bulmak
- 2010-2026 yillari arasinda yayinlanmis
- Calismada mutlaka sayisal metrikler olacak: yield, time, cost proxy gibi

Senin gorevin:
1. Scholar ve PubMed icin 3-4 farkli arama string'i oner (or. "cell-free protein synthesis AND yield AND microfluidic")
2. Cok genel olmamali, extraction yapilabilirligini onceliklendir
3. Gerekirse bir de 'biosensing CFPS' ya da 'toxic protein' odakli string oner

Her onerinin aciklamasini kisa notla birlikte ver.
```
