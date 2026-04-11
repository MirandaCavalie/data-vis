"""
Data Exploration & Cleaning Script
SF Eviction Notices Dataset
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
OUT_DIR    = os.path.join(BASE_DIR, "exploration_output")
CSV_IN     = os.path.join(DATA_DIR, "Eviction_Notices_20260403.csv")
CSV_OUT    = os.path.join(DATA_DIR, "evictions_cleaned.csv")

os.makedirs(OUT_DIR, exist_ok=True)

# ── 1. Load ────────────────────────────────────────────────────────────────────
print("=" * 65)
print("SF EVICTION NOTICES - DATA EXPLORATION")
print("=" * 65)

df = pd.read_csv(CSV_IN, low_memory=False)

print(f"\n[1] SHAPE:  {df.shape[0]:,} rows × {df.shape[1]} columns")
print("\n[2] COLUMNS & DTYPES:")
for col in df.columns:
    print(f"    {col:<40} {str(df[col].dtype):<12} nulls={df[col].isna().sum():,}")

print("\n[3] SAMPLE ROWS (first 3):")
print(df.head(3).to_string())

# ── 2. Data Quality ────────────────────────────────────────────────────────────
print("\n[4] NULL / MISSING PERCENTAGES:")
null_pct = (df.isna().sum() / len(df) * 100).round(2)
for col, pct in null_pct.items():
    if pct > 0:
        print(f"    {col:<40} {pct:>6.2f}%")

dup_count = df.duplicated().sum()
print(f"\n[5] DUPLICATE ROWS: {dup_count}")

# ── 3. Date Parsing ────────────────────────────────────────────────────────────
df['File Date'] = pd.to_datetime(df['File Date'], errors='coerce')
df['year']  = df['File Date'].dt.year
df['month'] = df['File Date'].dt.month

date_nulls = df['File Date'].isna().sum()
print(f"\n[6] DATE PARSING:")
print(f"    'File Date' nulls after parse: {date_nulls}")
print(f"    Date range: {df['File Date'].min().date()} to {df['File Date'].max().date()}")

# ── 4. Eviction Reason Columns ─────────────────────────────────────────────────
REASON_COLS = [
    'Non Payment', 'Breach', 'Nuisance', 'Illegal Use',
    'Failure to Sign Renewal', 'Access Denial', 'Unapproved Subtenant',
    'Owner Move In', 'Demolition', 'Capital Improvement',
    'Substantial Rehab', 'Ellis Act WithDrawal', 'Condo Conversion',
    'Roommate Same Unit', 'Other Cause', 'Late Payments',
    'Lead Remediation', 'Development', 'Good Samaritan Ends'
]

# Convert boolean strings to actual booleans
for col in REASON_COLS:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.lower().map(
            {'true': True, 'false': False, '1': True, '0': False}
        )

print("\n[7] EVICTION REASON COUNTS (sorted):")
reason_counts = {}
for col in REASON_COLS:
    if col in df.columns:
        cnt = df[col].sum()
        reason_counts[col] = int(cnt) if not pd.isna(cnt) else 0

for reason, cnt in sorted(reason_counts.items(), key=lambda x: -x[1]):
    print(f"    {reason:<35} {cnt:>6,}")

# ── 5. Derive primary_reason ───────────────────────────────────────────────────
def get_primary_reason(row):
    for col in REASON_COLS:
        if col in row and row[col] is True:
            return col
    return 'Unknown'

df['primary_reason'] = df.apply(get_primary_reason, axis=1)

print("\n[8] PRIMARY REASON DISTRIBUTION:")
pr_counts = df['primary_reason'].value_counts()
for reason, cnt in pr_counts.items():
    print(f"    {reason:<35} {cnt:>6,}  ({cnt/len(df)*100:.1f}%)")

# ── 6. Geographic Stats ────────────────────────────────────────────────────────
NBHD_COL = 'Neighborhoods - Analysis Boundaries'
print(f"\n[9] TOP 15 NEIGHBORHOODS BY EVICTION COUNT:")
if NBHD_COL in df.columns:
    top_nbhd = df[NBHD_COL].value_counts().head(15)
    for nbhd, cnt in top_nbhd.items():
        print(f"    {str(nbhd):<40} {cnt:>5,}")

# ── 7. Records per Year ────────────────────────────────────────────────────────
print("\n[10] RECORDS PER YEAR (1997–present):")
yearly = df.groupby('year').size().reset_index(name='count')
for _, row in yearly.iterrows():
    bar = '█' * int(row['count'] // 50)
    print(f"    {int(row['year'])}: {row['count']:>5,}  {bar}")

# ── 8. Clean & Export ──────────────────────────────────────────────────────────
df_clean = df.copy()

# Drop rows with no file date
before = len(df_clean)
df_clean = df_clean.dropna(subset=['File Date'])
print(f"\n[11] CLEANING:")
print(f"    Dropped {before - len(df_clean):,} rows with missing File Date")

# Drop rows with no neighborhood
before2 = len(df_clean)
df_clean = df_clean.dropna(subset=[NBHD_COL])
print(f"    Dropped {before2 - len(df_clean):,} rows with missing Neighborhood")

# Drop duplicates
before3 = len(df_clean)
df_clean = df_clean.drop_duplicates(subset=['Eviction ID'])
print(f"    Dropped {before3 - len(df_clean):,} duplicate Eviction IDs")

print(f"    Final clean dataset: {len(df_clean):,} rows")

df_clean.to_csv(CSV_OUT, index=False)
print(f"\n    Saved → {CSV_OUT}")

# ── 9. Exploratory Charts ──────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
PLOT_COLOR = "#2c7bb6"

# Chart 1: Evictions per year
fig, ax = plt.subplots(figsize=(12, 5))
yearly_clean = df_clean.groupby('year').size().reset_index(name='count')
ax.bar(yearly_clean['year'], yearly_clean['count'], color=PLOT_COLOR, edgecolor='white', linewidth=0.5)
ax.set_title("SF Eviction Notices Filed per Year", fontsize=14, fontweight='bold', pad=14)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Eviction Notices")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# Annotate key events
events = {2001: "Dot-com bust", 2008: "Financial crisis", 2016: "Tech boom peak", 2020: "COVID moratorium"}
for yr, label in events.items():
    yr_data = yearly_clean[yearly_clean['year'] == yr]
    if not yr_data.empty:
        cnt = yr_data['count'].values[0]
        ax.annotate(label, xy=(yr, cnt), xytext=(yr, cnt + 80),
                    fontsize=7.5, ha='center', color='#c0392b',
                    arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.8))

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "evictions_per_year.png"), dpi=150)
plt.close()
print(f"    Saved → exploration_output/evictions_per_year.png")

# Chart 2: Top eviction reasons
fig, ax = plt.subplots(figsize=(10, 6))
top_reasons = df_clean['primary_reason'].value_counts().head(10)
colors = sns.color_palette("Blues_r", len(top_reasons))
bars = ax.barh(top_reasons.index[::-1], top_reasons.values[::-1], color=colors[::-1])
ax.set_title("Top 10 Primary Eviction Reasons (SF, all years)", fontsize=14, fontweight='bold', pad=14)
ax.set_xlabel("Count")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
for bar, val in zip(bars, top_reasons.values[::-1]):
    ax.text(bar.get_width() + 30, bar.get_y() + bar.get_height() / 2,
            f"{val:,}", va='center', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "top_eviction_reasons.png"), dpi=150)
plt.close()
print(f"    Saved → exploration_output/top_eviction_reasons.png")

# Chart 3: Top neighborhoods
if NBHD_COL in df_clean.columns:
    fig, ax = plt.subplots(figsize=(10, 7))
    top15 = df_clean[NBHD_COL].value_counts().head(15)
    colors2 = sns.color_palette("YlOrRd", len(top15))
    bars2 = ax.barh(top15.index[::-1], top15.values[::-1], color=colors2[::-1])
    ax.set_title("Top 15 Neighborhoods by Total Eviction Notices", fontsize=14, fontweight='bold', pad=14)
    ax.set_xlabel("Count")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    for bar, val in zip(bars2, top15.values[::-1]):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va='center', fontsize=8.5)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "top_neighborhoods.png"), dpi=150)
    plt.close()
    print(f"    Saved → exploration_output/top_neighborhoods.png")

# Chart 4: Stacked area — reasons over time (top 6)
top6 = [r for r in df_clean['primary_reason'].value_counts().head(7).index if r != 'Unknown'][:6]
yearly_reason = df_clean[df_clean['year'] >= 1997].groupby(['year', 'primary_reason']).size().unstack(fill_value=0)
yearly_reason = yearly_reason[[c for c in top6 if c in yearly_reason.columns]]

fig, ax = plt.subplots(figsize=(13, 5))
palette = sns.color_palette("Set2", len(yearly_reason.columns))
ax.stackplot(yearly_reason.index, yearly_reason.T.values, labels=yearly_reason.columns, colors=palette, alpha=0.85)
ax.set_title("Eviction Reasons Over Time (Stacked Area)", fontsize=14, fontweight='bold', pad=14)
ax.set_xlabel("Year")
ax.set_ylabel("Count")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.legend(loc='upper right', fontsize=8, framealpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "reasons_stacked_area.png"), dpi=150)
plt.close()
print(f"    Saved → exploration_output/reasons_stacked_area.png")

print("\n" + "=" * 65)
print("EXPLORATION COMPLETE")
print("=" * 65)


# ── Print summary dict for PDF use ────────────────────────────────────────────
summary = {
    "total_records_raw":   df.shape[0],
    "total_records_clean": len(df_clean),
    "date_min":            str(df_clean['File Date'].min().date()),
    "date_max":            str(df_clean['File Date'].max().date()),
    "num_columns":         df.shape[1],
    "top_reason":          pr_counts.index[0],
    "top_reason_count":    int(pr_counts.iloc[0]),
    "top_nbhd":            top_nbhd.index[0] if NBHD_COL in df.columns else "N/A",
    "top_nbhd_count":      int(top_nbhd.iloc[0]) if NBHD_COL in df.columns else 0,
    "null_address_pct":    round(float(null_pct.get('Address', 0)), 2),
    "null_nbhd_pct":       round(float(null_pct.get(NBHD_COL, 0)), 2),
}

print("\n[SUMMARY FOR PDF]")
for k, v in summary.items():
    print(f"  {k}: {v}")
