"""Generate the benchmark charts shown in the README.

All inputs here are AGGREGATE metrics (accuracy percentages, measured latency,
representative list prices). No proprietary profiles or article text are used, so
this script and its PNG outputs are safe to publish.

Sources
-------
* Accuracy: 200-article held-out test, scored by relia-1 and by three frontier
  LLM raters (Gemini, ChatGPT, DeepSeek); ground truth = per-article median of
  the three raters ("consensus"). See validation/README.md.
* Speed: warm end-to-end latency measured against the hosted relia-1 endpoint
  (Cloud Run + L4); LLM figure is a typical per-article API round-trip.
* Cost: representative published list prices (input tokens), ~1.8K tokens/article.

Run:  python validation/make_charts.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

RELIA = "#00A98F"   # Relia brand teal
LLM = "#9aa0a6"     # neutral grey for LLM raters
ACCENT = "#1a73e8"

# Shared figure size + resolution so all charts render at a consistent, crisp size
# on GitHub (downscaled from 2x, so zooming stays sharp). bbox_inches="tight" on save
# keeps rotated y-axis titles from being clipped.
FIGSIZE = (9, 4.5)
DPI = 200

plt.rcParams.update({
    "font.size": 11.5,
    "axes.titlesize": 13,
    "axes.labelsize": 11.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.22,
    "axes.axisbelow": True,
    "figure.constrained_layout.use": False,
})


# --------------------------------------------------------------------------- #
# 1. Accuracy — agreement with the 3-LLM consensus (exact-bin %)              #
# --------------------------------------------------------------------------- #
def chart_accuracy():
    # exact-bin agreement with consensus (%)
    labels = ["Gemini", "ChatGPT", "DeepSeek", "Relia-1"]
    exact = [90.5, 90.0, 88.0, 86.5]
    colors = [LLM, LLM, LLM, RELIA]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(labels))
    bars = ax.bar(x, exact, color=colors, width=0.62)
    for b, v in zip(bars, exact):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.6, f"{v:.1f}%",
                ha="center", fontweight="bold")

    # the "how much do the LLMs even agree with EACH OTHER" band
    inter_lo, inter_hi = 78.0, 80.5
    ax.axhspan(inter_lo, inter_hi, color=ACCENT, alpha=0.10, zorder=0)
    ax.axhline(inter_hi, color=ACCENT, lw=1, ls="--", alpha=0.7)
    ax.text(1.5, inter_lo - 1.4,
            "LLM raters agree with each other only 78–80.5%",
            ha="center", color=ACCENT, fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Exact-bin agreement with 3-LLM consensus (%)")
    ax.set_ylim(70, 100)
    ax.set_title("Relia-1 matches a panel of frontier LLM raters\n"
                 "(200-article held-out test · grey = LLM raters, teal = Relia)",
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "accuracy.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / "accuracy.png")


# --------------------------------------------------------------------------- #
# 2. Accuracy detail — Relia across the three agreement metrics               #
# --------------------------------------------------------------------------- #
def chart_accuracy_detail():
    metrics = ["Exact bin", "Within 1 bin", "Relevant / not\n(binary)"]
    relia = [86.5, 100.0, 92.0]
    ceiling = [90.5, 100.0, 94.0]  # best LLM rater (Gemini) vs consensus

    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(metrics))
    w = 0.36
    b1 = ax.bar(x - w / 2, ceiling, w, label="Best LLM rater (ceiling)", color=LLM)
    b2 = ax.bar(x + w / 2, relia, w, label="Relia-1", color=RELIA)
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.6,
                    f"{b.get_height():.0f}", ha="center", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylabel("Agreement with consensus (%)")
    ax.set_ylim(0, 108)
    ax.legend(loc="lower right")
    ax.set_title("Relia-1 vs the LLM ceiling, by agreement metric",
                 fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "accuracy_detail.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / "accuracy_detail.png")


# --------------------------------------------------------------------------- #
# 3. Speed — per-article latency (log scale)                                  #
# --------------------------------------------------------------------------- #
def chart_speed():
    labels = ["Relia-1\n(batched)", "Relia-1\n(single call)", "Frontier LLM\n(per-article API)"]
    # measured: batch of 32 => 0.585s total => ~18 ms/article; single warm call ~0.41s
    ms = [18, 410, 1800]
    colors = [RELIA, RELIA, LLM]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(labels))
    bars = ax.bar(x, ms, color=colors, width=0.6)
    ax.set_yscale("log")
    for b, v in zip(bars, ms):
        txt = f"{v} ms" if v < 1000 else f"{v/1000:.1f} s"
        ax.text(b.get_x() + b.get_width() / 2, v * 1.12, txt,
                ha="center", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Time per article (ms, log scale)")
    ax.set_title("~100× faster per article than an LLM API call\n"
                 "(measured warm latency, hosted L4 endpoint)",
                 fontweight="bold")
    ax.set_ylim(8, 4000)
    fig.tight_layout()
    fig.savefig(OUT / "speed.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / "speed.png")


# --------------------------------------------------------------------------- #
# 4. Cost — $ per 1,000 articles                                              #
# --------------------------------------------------------------------------- #
def chart_cost():
    # $ to score 1,000 articles. ~1.8K input tokens/article => 1.8M input tokens per
    # 1,000 articles. LLM figures = current published INPUT-token list prices, verified
    # 2026-07 (anthropic.com, openai.com, ai.google.dev, api-docs.deepseek.com).
    tok_millions = 1.8
    price_in = {  # $ / 1M input tokens
        "Claude Sonnet 4": 3.00,
        "GPT-4o": 2.50,
        "Gemini 2.5 Flash": 0.30,
        "GPT-4o mini": 0.15,
        "DeepSeek-V4 Flash": 0.14,
    }
    sonnet = price_in["Claude Sonnet 4"] * tok_millions   # 5.40
    gpt4o = price_in["GPT-4o"] * tok_millions             # 4.50
    gem = price_in["Gemini 2.5 Flash"] * tok_millions     # 0.54
    mini = price_in["GPT-4o mini"] * tok_millions         # 0.27
    dsk = price_in["DeepSeek-V4 Flash"] * tok_millions    # 0.252
    # Relia API: $1 / 1,000 requests, up to 100 articles/request => $0.01 / 1,000 articles
    relia = 0.01

    labels = ["Claude Sonnet 4", "GPT-4o", "Gemini 2.5 Flash", "GPT-4o mini",
              "DeepSeek-V4 Flash", "Relia API"]
    vals = [sonnet, gpt4o, gem, mini, dsk, relia]
    colors = [LLM, LLM, LLM, LLM, LLM, RELIA]

    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(labels))
    bars = ax.bar(x, vals, color=colors, width=0.62)
    texts = [f"${sonnet:.2f}", f"${gpt4o:.2f}", f"${gem:.2f}", f"${mini:.2f}",
             f"${dsk:.2f}", f"${relia:.2f}"]
    for b, t in zip(bars, texts):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.12, t,
                ha="center", fontweight="bold", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Cost to score 1,000 articles (USD)")
    ax.set_title("Scoring articles yourself with LLM APIs vs the Relia API\n"
                 "(current published input-token list prices · ~1.8K input tokens/article)",
                 fontweight="bold")
    ax.set_ylim(0, max(vals) * 1.18)
    fig.tight_layout()
    fig.savefig(OUT / "cost.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / "cost.png")


if __name__ == "__main__":
    chart_accuracy()
    chart_accuracy_detail()
    chart_speed()
    chart_cost()
    print("done")
