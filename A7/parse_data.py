import csv
import os

base = os.path.dirname(os.path.abspath(__file__))

tvshow_path = os.path.join(base, "data_2", "fb-pages-tvshow.edges")
tvshow_out = os.path.join(base, "data_2", "edges.csv")

with open(tvshow_path, "r") as f_in, open(tvshow_out, "w", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["source", "target"])
    for line in f_in:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        src, tgt = int(parts[0]), int(parts[1])
        if src < 300 and tgt < 300:
            writer.writerow([src, tgt])

print("TV show edges written to data_2/edges.csv")

congress_path = os.path.join(base, "data_1", "congress.edgelist")
congress_out = os.path.join(base, "data_1", "edges.csv")

with open(congress_path, "r") as f_in, open(congress_out, "w", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["source", "target"])
    for line in f_in:
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ")
        src, tgt = int(parts[0]), int(parts[1])
        if src < 92 and tgt < 92:
            writer.writerow([src, tgt])

print("Congress edges written to data_1/edges.csv")
