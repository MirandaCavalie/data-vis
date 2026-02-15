# A3 - Visualizing Distributions using P5.js

## Dataset
**Daily Screen Time Usage** — 2,800 records with variables like total screen time, social media hours, work/study hours, entertainment hours, and age.

## How to View
Open `index.html` in a browser or deploy to GitHub Pages. The index page links to all individual charts.

> **Note:** If opening locally, use a local server (e.g. `python -m http.server`) since P5 loads CSV files via fetch.

## Features Completed
| Requirement | Status |
|---|---|
| Histogram (P5 + Seaborn) | ✅ |
| Labeled axes + grid | ✅ |
| Box Plot (P5 + Seaborn) | ✅ |
| Strip Chart with jitter (P5 + Seaborn) | ✅ |
| Outlier highlighting on box plot | ✅ |
| Interactive tooltips on histogram | ✅ |
| Interactive tooltips on ALL charts (extra credit) | ✅ |
| ECDF chart (extra credit) | ✅ |

## Folder Structure
```
A3-Visualizing-Distributions/
├── index.html              # Main landing page with links to all charts
├── README.md
├── seaborn_charts.py       # Python script to generate seaborn screenshots
├── data/
│   └── daily_usage.csv     # Trimmed CSV (5 columns, ~54KB)
├── p5/
│   ├── histogram.html      # P5 histogram (total_screen_time)
│   ├── boxplot.html        # P5 box plot with outliers (work_or_study_hours)
│   ├── stripchart.html     # P5 strip chart with jitter (entertainment_hours)
│   └── ecdf.html           # P5 ECDF chart (social_media_hours)
└── screenshots/
    ├── seaborn_histogram.png
    ├── seaborn_boxplot.png
    └── seaborn_stripplot.png
```
