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

```
.github/workflows/digest.yml   → Defines the weekly schedule (cron)
digest.py                      → Fetches data from all sources and sends the email
requirements.txt               → Python dependencies
```

## Setup

If you want to run your own copy of this digest:

1. Fork or clone this repository
2. Go to **Settings → Secrets and variables → Actions** and add the following repository secrets:

   | Secret | Description |
   |---|---|
   | `MAIL_FROM` | The Gmail address the digest will be sent from |
   | `MAIL_PASSWORD` | A Gmail [App Password](https://myaccount.google.com/apppasswords) (not your regular password) |
   | `MAIL_TO` | The email address that should receive the digest |
   | `PRODUCTHUNT_TOKEN` | A [Product Hunt Developer Token](https://api.producthunt.com/v2/oauth/applications) |

3. That's it — the workflow will run automatically every Monday. You can also trigger it manually from the **Actions** tab using **Run workflow**.

## Customization

- **Change the schedule:** edit the `cron` expression in `.github/workflows/digest.yml` ([crontab.guru](https://crontab.guru/) is helpful for this)
- **Add or remove sources:** each source is its own function in `digest.py` (`get_hn_top_stories`, `get_producthunt_trending`, `get_lennys_newsletter`) — add a new function following the same pattern to include another source
- **Change the number of items per source:** adjust the `limit` parameter in each function

## Notes

- All credentials are stored securely as GitHub Actions secrets — nothing is hardcoded in the source code.
- If one data source fails (e.g. an API is temporarily down), the digest still sends with the remaining sources — failures are caught and reported inline rather than blocking the whole email.
