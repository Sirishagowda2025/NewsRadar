# 📡 NewsRadar — AI-Powered Industry Intelligence Monitor

> Automatically scrapes, scores, and summarises industry news using a local LLM — then delivers a polished, interactive HTML digest you can review, curate, and email to your team in one click.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-local%20LLM-black?logo=ollama)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 🔍 What It Does

NewsRadar is an **end-to-end intelligence pipeline** that monitors hundreds of Google News RSS feeds, filters out noise, and uses a local AI model to score and summarise only the articles that matter — delivering them as a beautiful, interactive HTML report.

It was built to solve a real problem: **manually reading dozens of industry news sources every day is slow, inconsistent, and easy to miss things that matter.** NewsRadar automates the whole workflow.

```
RSS Feeds (100+ queries)
        │
        ▼
┌───────────────────┐
│  Gate 0: Source   │  Block irrelevant domains (tabloids, social media, PR wires)
│  blocklist        │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Gate 1: Keyword  │  Drop articles matching noise keywords (IPOs, celebrity, etc.)
│  exclude filter   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Gate 2: Keyword  │  Must contain at least one relevance keyword to proceed
│  relevance filter │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Deduplication    │  Fuzzy headline match + URL + snippet fingerprint
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Gate 3: AI Score │  Local LLM scores 0–10 for business relevance
│  (Ollama qwen3)   │  Articles below threshold are dropped
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  AI Summarisation │  LLM generates 4 specific bullet-point facts per article
└────────┬──────────┘
         │
         ▼
  Interactive HTML Report + Excel Export + Email Digest
```

---

## ✨ Features

- **100% local AI** — uses [Ollama](https://ollama.com) with `qwen3:4b`. No OpenAI API key, no cloud costs, no data leaving your machine.
- **Multi-gate filtering pipeline** — four sequential filters before AI scoring to minimise wasted LLM calls and keep quality high.
- **Feedback learning loop** — your Keep / Remove clicks are saved and injected into future AI scoring prompts, so the model adapts to your preferences over time.
- **Interactive HTML report** with drag-and-drop card reordering across categories, editable report title, and one-click email send.
- **Sequential RSS fetching** — one query at a time to keep CPU usage low (no thread-bombing).
- **CPU-aware LLM calls** — Ollama is capped to half your logical core count; scoring uses a 60-token budget vs 400 for summaries.
- **Excel export** — every article with AI score, reason, and summary bullets exported to `.xlsx`.
- **Configurable for any industry** — all search queries, keywords, and categories live in `config.py`. Swap them out and it works for fintech, healthcare, SaaS, or anything else.

---

## 🖥️ Demo Preview

![NewsRadar Demo](screenshot.png)

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running (`ollama serve`)
- The AI model pulled: `ollama pull qwen3:4b`

### 2. Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/newsradar.git
cd newsradar
pip install feedparser openpyxl ollama python-dotenv
```

### 3. Configure secrets

```bash
cp .env.example .env
# Open .env and fill in your email credentials
```

> **Gmail users:** You need a [Gmail App Password](https://myaccount.google.com/apppasswords), not your regular password. Enable 2-Step Verification first, then generate an App Password for "Mail".

### 4. Run

```bash
python main.py
```

The report opens automatically in your browser. Review articles, drag to reorder, click ✕ to remove noise, edit the report title — then hit **✉ Send Email**.

### 5. Send on a schedule (optional)

Add to cron for daily digests:

```bash
# Every day at 8am
0 8 * * * cd /path/to/newsradar && python main.py
```

---

## ⚙️ Configuration

All settings live in `config.py` and `.env`.

| Setting | Where | Default | Description |
|---|---|---|---|
| `time_window_hours` | `config.py` | `168` | How far back to fetch news (168 = 1 week) |
| `articles_per_category` | `config.py` | `20` | Max articles kept per section after AI ranking |
| `MIN_RELEVANCE_SCORE` | `.env` | `7` | AI score threshold (0–10). Lower = more articles |
| `OLLAMA_MODEL` | `.env` | `qwen3:4b` | Any model you have pulled in Ollama |
| `AI_ENABLED` | `.env` | `true` | Set to `false` to skip AI (faster, no Ollama needed) |

### Adapting to a different industry

1. Open `config.py`
2. Update `CATEGORIES` → `search_queries` with relevant Google News search terms
3. Update `RELEVANCE_KEYWORDS` to match terms important to your domain
4. Update `EXCLUDE_KEYWORDS` to block noise specific to your industry

---

## 📁 Project Structure

```
newsradar/
├── main.py              # Entry point — runs the full pipeline
├── config.py            # All categories, keywords, and settings
├── .env                 # Your actual secrets (gitignored — never committed)
└── README.md
```

---

## 🧠 How the AI Scoring Works

Each article is sent to a local LLM with a carefully engineered prompt that defines:

- What scores 8–10 (directly actionable: fee changes, compliance deadlines, API updates)
- What scores 5–7 (useful context: market trends, infrastructure news)
- What scores 0–4 (irrelevant: IPOs, celebrity, how-to guides)

The prompt also includes examples from your past Keep / Remove feedback, so the model gradually learns what *you* care about.

Scoring uses only 60 output tokens (fast). Summarisation uses 400 tokens (4 detailed bullet points).

---

## 🔒 Security Notes

- **Never commit `.env`** — it's in `.gitignore` by default.
- Email credentials (SMTP password) live only in `.env`, never in source code.
- The local Ollama server runs on `127.0.0.1` — no data leaves your machine.
- The feedback HTTP server also binds to `127.0.0.1` only.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| News source | Google News RSS via `feedparser` |
| AI scoring & summarisation | Ollama (`qwen3:4b`) — runs 100% locally |
| Deduplication | `difflib.SequenceMatcher` (fuzzy match) |
| Report UI | Vanilla HTML + CSS + JavaScript (drag-and-drop, no framework) |
| Email delivery | Python `smtplib` + `email.mime` |
| Data export | `openpyxl` (Excel) |
| Local server | Python `http.server` (feedback + email trigger) |

---

## 📈 Potential Extensions

- [ ] Add a web UI (Flask / FastAPI) to configure categories without editing code
- [ ] Support multiple industries simultaneously with a profile switcher
- [ ] Slack / Teams webhook delivery alongside email
- [ ] Sentiment analysis layer on top of AI scoring
- [ ] SQLite persistence for article history and trend tracking
- [ ] Docker container for zero-setup deployment

---

## 📄 License

MIT — free to use, modify, and distribute. See [LICENSE](LICENSE).

---

## 🙋 About

Built as an internship project to automate competitive intelligence monitoring for an e-commerce operations team. Repurposed and open-sourced as a general-purpose industry news monitor.

*Questions or suggestions? Open an issue or reach out on [LinkedIn](https://www.linkedin.com/in/sirisha-d-064b69278/).*
