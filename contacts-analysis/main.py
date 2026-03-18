import numpy as np
import json
import os
from collections import defaultdict

## load the moon links from the json file

moon_links = []
with open("moon_links.json", "r", encoding="utf-8") as f:
    moon_links = json.load(f)

## --- Contact analysis per satellite ---

def find_contact_windows(bool_times):
    """
    Given a sorted list of (time, bool) pairs, return a list of (start, end) tuples
    representing contiguous contact windows where bool is True.
    """
    windows = []
    in_window = False
    start = None
    for t, active in bool_times:
        if active and not in_window:
            start = t
            in_window = True
        elif not active and in_window:
            windows.append((start, t - 30))  # last active step was t-30
            in_window = False
    if in_window:
        windows.append((start, bool_times[-1][0]))
    return windows

def merge_windows(windows):
    """Merge overlapping or adjacent contact windows (tolerance: 30s step)."""
    if not windows:
        return []
    sorted_w = sorted(windows)
    merged = [sorted_w[0]]
    for start, end in sorted_w[1:]:
        if start <= merged[-1][1] + 30:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged

# Group entries by satellite
sat_data = defaultdict(list)
for entry in moon_links:
    sat_data[entry["sat_id"]].append(entry)

rows = []
for sat_id, entries in sorted(sat_data.items()):
    all_windows = []
    active_distances = []
    for entry in entries:
        bool_times = [(t["time"], t["bool"]) for t in entry["times"]]
        if not bool_times:
            continue

        active_distances.extend(t["dist"] for t in entry["times"] if t["bool"])
        windows = find_contact_windows(bool_times)
        all_windows.extend(windows)

    merged = merge_windows(all_windows)

    if not merged:
        rows.append((sat_id, None, None, None, None))
        continue

    durations = [end - start for start, end in merged]
    avg_duration_min = np.mean(durations) / 60
    num_windows = len(merged)

    gaps = [merged[i+1][0] - merged[i][1] for i in range(len(merged) - 1)]
    max_gap_h = max(gaps) / 3600 if gaps else 0.0
    avg_distance = np.mean(active_distances) if active_distances else None

    rows.append((sat_id, avg_duration_min, num_windows, max_gap_h, avg_distance))

print(r"\begin{table}[ht]")
print(r"  \centering")
print(r"  \begin{tabular}{lrrrr}")
print(r"    \toprule")
print(r"    Satellite & Avg.\ contact (min) & Nb.\ windows & Max gap (h) & Avg.\ dist. (km) \\")
print(r"    \midrule")
for sat_id, avg_min, num_w, max_gap, avg_dist in rows:
    if avg_min is None:
        print(f"    {sat_id} & -- & -- & -- & -- \\\\")
    else:
        print(f"    {sat_id} & {avg_min:.1f} & {num_w} & {max_gap:.2f} & {avg_dist:.1f} \\\\")
print(r"    \bottomrule")
print(r"  \end{tabular}")
print(r"  \caption{Average contact window duration, maximum blackout gap, and average link distance per satellite.}")
print(r"  \label{tab:satellite-contacts}")
print(r"\end{table}")


