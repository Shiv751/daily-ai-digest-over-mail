# 🤖 Daily AI News Digest — Setup Guide

Sends a beautifully formatted AI news digest to your email every day at **10:00 AM IST**, powered by GitHub Actions + NewsAPI.

---

## 📁 Files

```
├── send_digest.py                        # Main Python script
└── .github/
    └── workflows/
        └── daily_digest.yml             # GitHub Actions scheduler
```

---

## 🚀 Setup Steps

### Step 1 — Get a Free NewsAPI Key
1. Go to [https://newsapi.org](https://newsapi.org) and sign up (free)
2. Copy your API key from the dashboard

### Step 2 — Enable Gmail App Password
> Required because Gmail blocks plain passwords for scripts.

1. Go to your Google Account → **Security**
2. Enable **2-Step Verification** (if not already)
3. Search for **"App Passwords"** → Create one for "Mail"
4. Copy the 16-character password generated

### Step 3 — Create a GitHub Repository
1. Go to [https://github.com/new](https://github.com/new)
2. Create a new **private** repository (e.g., `ai-daily-digest`)
3. Upload both files maintaining the folder structure:
   - `send_digest.py` → root of repo
   - `.github/workflows/daily_digest.yml` → exactly this path

### Step 4 — Add GitHub Secrets
1. In your repo, go to **Settings → Secrets and variables → Actions**
2. Click **"New repository secret"** and add all 4:

| Secret Name        | Value                          |
|--------------------|--------------------------------|
| `RECIPIENT_EMAIL`  | Your email address             |
| `SENDER_EMAIL`     | Your Gmail address             |
| `SENDER_PASSWORD`  | Gmail App Password (Step 2)    |
| `NEWS_API_KEY`     | NewsAPI key (Step 1)           |

### Step 5 — Test It Manually
1. Go to **Actions** tab in your GitHub repo
2. Click **"Daily AI News Digest"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Check your inbox within 30 seconds ✅

---

## ⏰ Schedule
Runs automatically every day at **10:00 AM IST** (4:30 AM UTC).
No server needed — GitHub hosts and runs it for free.

---

## 📧 Email Preview
- Clean, formatted HTML email
- Top 8 AI stories with title, source, date & summary
- Direct links to full articles
