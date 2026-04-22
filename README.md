# 📡 NewsRadar — AI-Powered Industry Intelligence Monitor

> Automatically scrapes, scores, and summarises industry news using a local LLM — then delivers a polished, interactive HTML digest you can review, curate, and email to your team in one click.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-local%20LLM-black)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-2.0-brightgreen)

---

## 🖥️ Demo

![NewsRadar Demo](screenshot.png)

---

## 🔍 What It Does

NewsRadar is an **end-to-end intelligence pipeline** that monitors hundreds of Google News RSS feeds, filters out noise, and uses a local AI model to score and summarise only the articles that matter — delivering them as a beautiful, interactive HTML report.

Built to solve a real problem: **manually reading dozens of industry news sources every day is slow, inconsistent, and easy to miss things that matter.**

```
RSS Feeds (100+ queries per industry)
        │
        ▼
┌───────────────────┐
│  Gate 0           │  Block irrelevant domains (tabloids, social media, PR wires)
└────────┬──────────┘
         ▼
┌───────────────────┐
│  Gate 1           │  Drop articles matching noise keywords (IPOs, celebrity, etc.)
└────────┬──────────┘
         ▼
┌───────────────────┐
│  Gate 2           │  Must contain at least one relevance keyword to proceed
└────────┬──────────┘
         ▼
┌───────────────────┐
│  Deduplication    │  Fuzzy headline match (78%) + URL + snippet fingerprint
└────────┬──────────┘
         ▼
┌───────────────────┐
│  AI Score         │  Local LLM scores 0-10. Below threshold = dropped.
└────────┬──────────┘
         ▼
┌───────────────────┐
│  AI Summarise     │  4 specific bullet-point facts generated per article
└────────┬──────────┘
         ▼
  Interactive HTML Report + Excel Export + Email + Slack
```

---

## Features

| Feature | Description |
|---|---|
| Multi-industry profiles | Switch between `ecommerce`, `fintech`, `healthcare`, `tech` with one flag |
| Live search bar | Filter all cards across all sections in real time as you type |
| Score + date filters | Show only AI 5+ / 7+ / 9+ articles or filter by today / this week |
| Dark mode | One-click toggle in the topbar |
| Slack webhook | Auto-posts a digest to your Slack channel after every run |
| 100% local AI | Uses Ollama — no OpenAI key, no cloud costs, no data leaving your machine |
| Feedback learning | Keep/Remove clicks feed into future AI scoring prompts |
| One-click email | Review, reorder, edit title, send — all from the browser |
| Drag-and-drop | Move articles between categories before sending |
| Excel export | Full data with AI scores and summaries exported to `.xlsx` |

---

## Quick Start

### Step 1 — Install Python requirements

```bash
pip install feedparser openpyxl ollama requests python-dotenv
```

### Step 2 — Install Ollama and pull the AI model

Download Ollama from [ollama.com](https://ollama.com) and install it.

Start the Ollama server (keep this terminal open):

```bash
ollama serve
```

In a new terminal, pull the AI model (one-time download, ~2.5 GB):

```bash
ollama pull qwen3:4b
```

### Step 3 — Configure your credentials

Copy the example env file:

```bash
cp .env.example .env
```

Open `.env` in any text editor and fill in these three values at minimum:

```
SENDER_EMAIL=you@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
RECIPIENTS=you@gmail.com
```

**Where to get your Gmail App Password:**
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Enable 2-Step Verification on your Google account if not already on
3. Click "Create" and select "Mail" as the app
4. Copy the 16-character code it gives you (looks like `abcd efgh ijkl mnop`)
5. Paste that as your `SMTP_PASSWORD` — do **not** use your normal Gmail password

### Step 4 — Run

```bash
python main.py
```

The report opens automatically in your browser at `http://127.0.0.1:5765`.

From the report you can:
- **Search** articles by keyword using the search bar
- **Filter** by AI score (5+ / 7+ / 9+) or date (today / this week)
- **Toggle dark mode** with the moon button in the top right
- **Drag cards** to reorder or move between categories
- **Click Remove** to delete articles you don't want
- **Edit the report title** by clicking on it
- **Click Send Email** to email the final digest to all recipients

---

## Switching Industries

Use the `--industry` flag to monitor a different sector:

```bash
python main.py                        # E-commerce India (default)
python main.py --industry fintech     # Payments, lending, crypto regulation
python main.py --industry healthcare  # Drug regulation, health tech policy
python main.py --industry tech        # AI/LLM policy, cloud pricing, cybersecurity
```

To add your own custom industry, add an entry to `INDUSTRY_PROFILES` in `main.py` with your own search queries and keywords.

---

## Slack Integration (Optional)

1. Create a Slack Incoming Webhook: [api.slack.com/messaging/webhooks](https://api.slack.com/messaging/webhooks)
2. Add to your `.env`:

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

NewsRadar will post a compact digest (top article per category) to Slack automatically after each run.

---

## Configuration Reference

| Setting | File | Default | Description |
|---|---|---|---|
| `time_window_hours` | `config.py` | `168` | How far back to fetch news. 24 = daily, 168 = weekly, 720 = monthly |
| `articles_per_category` | `config.py` | `20` | Max articles kept per section after AI ranking |
| `MIN_RELEVANCE_SCORE` | `.env` | `7` | AI score threshold 0-10. Lower number = more articles pass through |
| `OLLAMA_MODEL` | `.env` | `qwen3:4b` | Any model you have pulled in Ollama |
| `AI_ENABLED` | `.env` | `true` | Set to `false` to skip AI scoring entirely (much faster, no Ollama needed) |
| `SLACK_WEBHOOK_URL` | `.env` | blank | Slack webhook URL. Leave blank to disable |

---

## Project Structure

```
newsradar/
├── main.py          # Full pipeline: scraper, AI scoring, HTML report, local server
├── config.py        # Categories, search queries, and keyword filter lists
├── .env.example     # Template showing all environment variables (safe to commit)
├── .env             # Your actual credentials (gitignored, never committed)
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| News source | Google News RSS via `feedparser` |
| AI scoring and summarisation | Ollama with `qwen3:4b` running locally |
| Deduplication | `difflib.SequenceMatcher` fuzzy headline matching |
| Report UI | Vanilla HTML, CSS, and JavaScript — no framework |
| Email | Python `smtplib` with MIME |
| Slack | Incoming Webhooks via `requests` |
| Excel export | `openpyxl` |

---

## Troubleshooting

**"RSS entries found: 0"**
Google News occasionally rate-limits requests. Wait 5 minutes and try again.

**"AI SKIP — cannot reach Ollama"**
Make sure Ollama is running. Open a terminal and run `ollama serve`, then keep that terminal open while running the script.

**"SMTP Authentication Error" when sending email**
You must use a Gmail App Password, not your regular Gmail login password. Follow the steps in Step 3 above.

**Report does not open automatically in browser**
Open your browser manually and navigate to `http://127.0.0.1:5765`

**Script runs but finds 0 articles**
Lower `MIN_RELEVANCE_SCORE` to `5` in your `.env`, or set `AI_ENABLED=false` to skip the AI gate entirely and see all keyword-matched articles.

---

## Roadmap

- [ ] Web UI to configure categories without editing code
- [ ] SQLite persistence for article history and trend tracking
- [ ] Docker container for zero-setup deployment
- [ ] WhatsApp and Teams notification support
- [ ] Sentiment trend graph across weeks

---

## License

MIT — free to use, modify, and distribute.

---

## About

Built during an internship to automate competitive intelligence monitoring for an e-commerce operations team. Open-sourced as a general-purpose industry news monitor supporting multiple industries.

*Questions or suggestions? Open an issue or reach out on [LinkedIn](https://linkedin.com/in/YOUR_PROFILE).*
