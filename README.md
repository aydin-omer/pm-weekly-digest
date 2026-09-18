# 📬 PM Weekly Digest

An automated weekly digest for product managers, delivered straight to your inbox every Monday morning.

## What it does

Every Monday at 08:30 (Turkey time), this project automatically:

1. **Fetches top stories** from [Hacker News](https://news.ycombinator.com/)
2. **Fetches trending products** from [Product Hunt](https://www.producthunt.com/)
3. **Fetches the latest posts** from [Lenny's Newsletter](https://www.lennysnewsletter.com/)
4. Compiles everything into a single, clean email and sends it via Gmail

No manual work required — it just runs in the background, forever, for free.

## Why

As a Product Manager, staying on top of industry trends, new tools, and thought leadership content is important but time-consuming. This digest automates that discovery process so the highlights land in your inbox instead of requiring active browsing.

## How it works

- **Language:** Python
- **Automation:** [GitHub Actions](https://github.com/features/actions) scheduled workflow (cron job)
- **Email delivery:** Gmail SMTP
- **No server required** — runs entirely on GitHub's free infrastructure

## Architecture
