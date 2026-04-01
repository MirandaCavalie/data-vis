"""
Seaborn Charts for A3 - Visualizing Distributions
Generates: histogram, box plot, and strip chart as PNG screenshots.
Dataset: Daily Screen Time Usage
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load data
df = pd.read_csv('data/daily_usage.csv')
os.makedirs('screenshots', exist_ok=True)

# Set a clean style
sns.set_theme(style="whitegrid")

# --- 1. Histogram: Total Screen Time ---
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x='total_screen_time', bins=20, color='steelblue', edgecolor='white', ax=ax)
ax.set_xlabel('Total Screen Time (hours)', fontsize=13)
ax.set_ylabel('Frequency', fontsize=13)
ax.set_title('Distribution of Total Screen Time', fontsize=15)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('screenshots/seaborn_histogram.png', dpi=150)
plt.close()
print("Saved: screenshots/seaborn_histogram.png")

# --- 2. Box Plot: Work or Study Hours ---
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, y='work_or_study_hours', color='lightcoral', width=0.4, ax=ax)
ax.set_ylabel('Work or Study Hours', fontsize=13)
ax.set_title('Box Plot of Work or Study Hours', fontsize=15)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('screenshots/seaborn_boxplot.png', dpi=150)
plt.close()
print("Saved: screenshots/seaborn_boxplot.png")

# --- 3. Strip Plot: Entertainment Hours ---
fig, ax = plt.subplots(figsize=(10, 6))
sns.stripplot(data=df, y='entertainment_hours', color='mediumseagreen', jitter=0.35, alpha=0.4, size=4, ax=ax)
ax.set_ylabel('Entertainment Hours', fontsize=13)
ax.set_title('Strip Chart of Entertainment Hours', fontsize=15)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('screenshots/seaborn_stripplot.png', dpi=150)
plt.close()
print("Saved: screenshots/seaborn_stripplot.png")

print("\nAll seaborn charts saved to screenshots/ folder.")
