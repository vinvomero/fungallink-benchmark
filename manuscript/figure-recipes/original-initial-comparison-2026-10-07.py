"""Regenerate this draft figure from the two frozen result JSON files.

Run from any directory: python /path/to/initial-comparison-2026-10-07.py
Requires matplotlib 3.11.0 (the version used for the recorded rendering).
"""

import hashlib
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULTS = ROOT / "data/processed/source-selected-gcf-analysis-v1-results"
SOURCES = [RESULTS / "deterministic-summary.json", RESULTS / "shared-random.json"]
rows, random = [json.loads(path.read_text(encoding="utf-8")) for path in SOURCES]
PRIMARY = "draft_all_source_observations"
METHODS = [
    ("global_prevalence", "Global prevalence"),
    ("prevalence_difference", "Prevalence difference"),
    ("metcalf_raw", "Raw Metcalf"),
    ("metcalf_standardized", "Standardized Metcalf"),
    ("uniform_random", "Uniform random (exact)"),
]
METRICS = [("hit@10", "A   Expected hit@10"), ("rr", "B   Mean expected reciprocal rank")]
assert len(rows) == 72
rosters = {row["roster"] for row in rows}
assert len(rosters) == 18 and PRIMARY in rosters
assert len(random["exact_queries"]) == 5
assert sum(query["product_count"] for query in random["exact_queries"]) == 6
assert {query["pool_size"] for query in random["exact_queries"]} == {9339}
assert random["overall"]["group_count"] == 1

# Each tuple is (primary estimate, minimum over all 18 rosters, maximum).
values = {}
for method, label in METHODS:
    for metric, title in METRICS:
        if method == "uniform_random":
            exact = random["overall"]["metrics"][metric]["exact_expectation"]
            values[method, metric] = (exact, exact, exact)
        else:
            selected = [row for row in rows if row["method"] == method]
            assert len(selected) == 18
            assert {row["roster"] for row in selected} == rosters
            for row in selected:
                summary = row["summary"]
                assert summary["query_count"] == 5 and summary["group_count"] == 1
                assert summary["coverage"] == 1
                assert summary["conditional"]["metrics"] == summary["end_to_end"]["metrics"]
            estimates = [row["summary"]["end_to_end"]["metrics"][metric] for row in selected]
            primary = next(row for row in selected if row["roster"] == PRIMARY)
            point = primary["summary"]["end_to_end"]["metrics"][metric]
            values[method, metric] = (point, min(estimates), max(estimates))

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.labelsize": 10, "axes.titlesize": 11,
    "svg.fonttype": "none", "svg.hashsalt": "fungallink-initial-2026-10-07",
    "pdf.fonttype": 42, "ps.fonttype": 42,
})
teal, gray, ink = "#087F83", "#A8ADAF", "#252A2C"
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.35), sharey=True)
fig.subplots_adjust(left=0.225, right=0.985, bottom=0.26, top=0.77, wspace=0.20)
for panel, (ax, (metric, title)) in enumerate(zip(axes, METRICS)):
    scale = 1 if metric == "hit@10" else 0.30
    for index, (method, label) in enumerate(METHODS):
        point, low, high = values[method, metric]
        y = len(METHODS) - 1 - index
        if high > low:
            ax.plot([low, high], [y, y], color=gray, linewidth=4, solid_capstyle="round", zorder=2)
            ax.plot([low, high], [y, y], linestyle="none", marker="|", markersize=9, color=gray, zorder=2)
        ax.plot(point, y, "o", color=teal, markersize=6, markeredgecolor="white", markeredgewidth=0.7, zorder=3)
        number = "0" if point == 0 else (f"{point:.6f}" if point < 0.01 else f"{point:.3f}")
        ax.text(high + scale * 0.027, y, number, va="center", fontsize=9, color=ink)
    ax.set_title(title, loc="left", pad=16, fontweight="bold", color=ink)
    ax.set_xlim(-scale * 0.025, scale * 1.055)
    ax.set_ylim(-0.5, 4.5)
    ticks = [0, .2, .4, .6, .8, 1] if metric == "hit@10" else [0, .1, .2, .3]
    ax.set_xticks(ticks)
    ax.set_xticklabels(["0" if value == 0 else f"{value:.1f}" for value in ticks])
    ax.set_yticks(range(5), [label for _, label in reversed(METHODS)])
    ax.grid(axis="x", color="#ECEEEE", linewidth=0.7, zorder=0)
    ax.tick_params(axis="both", length=0, pad=7, colors=ink)
    for spine in ["top", "left", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#BDC2C3")
fig.text(0.02, 0.94, "Source-selected fungal GCF retrieval", fontsize=15, fontweight="bold", color=ink)
fig.text(0.02, 0.875, "5 queries  |  6 supported products  |  9,339 candidates  |  1 conservative group", fontsize=10, color="#52595C")
legend = [
    Line2D([0], [0], marker="o", linestyle="none", color=teal, markersize=6, label="Primary roster (105 observations)"),
    Line2D([0], [0], color=gray, linewidth=4, label="Min–max across all 18 rosters"),
]
fig.legend(handles=legend, loc="lower left", bbox_to_anchor=(0.217, 0.11), frameon=False, ncol=2, fontsize=9)
fig.text(0.225, 0.065, "Ranges describe roster sensitivity; they are not confidence intervals.", fontsize=9, color="#52595C")
fig.text(0.225, 0.021, "Retrospective comparison. Exact random expectations are shared across rosters.", fontsize=9, color="#52595C")
stem = HERE / "initial-comparison-2026-10-07"
for extension in ["svg", "pdf", "png"]:
    metadata = {"Date": None} if extension == "svg" else ({"CreationDate": None, "ModDate": None} if extension == "pdf" else {})
    fig.savefig(stem.with_suffix("." + extension), dpi=300, facecolor="white", metadata=metadata)
plt.close(fig)

caption = """# Figure caption

Source-selected retrospective retrieval of supported fungal GCF products. (A) Expected hit@10 and (B) mean expected reciprocal rank summarize five queries with six supported products, 9,339 measured candidates per query and one conservative analysis group. Teal points show the primary roster of 105 source-study observations; gray segments show the minimum and maximum across all 18 overlapping rosters, including the primary roster. These ranges describe roster sensitivity and are not confidence intervals. Labels give primary estimates. Uniform-random points are exact expectations shared across rosters. Scores receive expected credit under uniform ordering within exact ties; hit@10 concerns at least one supported product, and reciprocal rank concerns the first supported product. All deterministic rankings covered all five queries. The observations and queries do not establish independent biological replicates, and the figure supports no significance or winner claim. Source-informed family selection and prior exposure limit interpretation.

# Production provenance (outside the paper caption)

This private publication draft reads the frozen JSON results directly; it does not rerun scoring or simulation. Deterministic values use `summary.end_to_end.metrics` (equal to conditional metrics at complete coverage); random values use `overall.metrics.*.exact_expectation`, not simulation means. Gray ranges include every roster without selecting representative choices. Very small ranges may be hidden by the primary point at the displayed scale. The two Metcalf scores are related variants. Frozen workflows are version 0.1.0.

Regenerate from any working directory with `python /path/to/manuscript/figures/initial-comparison-2026-10-07.py`. The recipe writes SVG, PDF, PNG and this caption in its own directory.

"""
caption += f"Rendering environment: Python {platform.python_version()}; Matplotlib {matplotlib.__version__}; DejaVu Sans; 10.5 × 4.35 inches; PNG at 300 dpi.\n\n"
caption += "Source SHA-256 checksums:\n\n"
for path in SOURCES:
    caption += f"- `{path.relative_to(ROOT).as_posix()}`: `{hashlib.sha256(path.read_bytes()).hexdigest()}`\n"
caption += "\nExact plotted values (primary; all-roster minimum; all-roster maximum):\n\n"
caption += "| Workflow | Metric | Primary | Minimum | Maximum |\n|---|---|---:|---:|---:|\n"
for method, label in METHODS:
    for metric, title in METRICS:
        point, low, high = values[method, metric]
        caption += f"| {label} | {metric} | {point:.17g} | {low:.17g} | {high:.17g} |\n"
caption += "\nRequested authoring route: gpt-6-astra / medium. No serving-side receipt was exposed, so the actual serving model and effort remain unverified.\n"
stem.with_name(stem.name + "-caption.md").write_text(caption, encoding="utf-8")
print(json.dumps({f"{method}/{metric}": value for (method, metric), value in values.items()}, indent=2))
