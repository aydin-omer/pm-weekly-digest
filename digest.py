import requests
import feedparser
import os
import smtplib
from email.mime.text import MIMEText

# ---------- Hacker News ----------
def get_hn_top_stories(limit=5):
    ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids = requests.get(ids_url, timeout=10).json()[:limit]

    stories = []
    for story_id in ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        item = requests.get(item_url, timeout=10).json()
        title = item.get("title", "No title")
        link = item.get("url", f"https://news.ycombinator.com/item?id={story_id}")
        score = item.get("score", 0)
        stories.append(f"- {title} ({score} points)\n  {link}")

    return "\n".join(stories) if stories else "No stories found."


# ---------- Product Hunt ----------
def get_producthunt_trending(limit=5):
    token = os.environ.get("PRODUCTHUNT_TOKEN")
    if not token:
        return "Product Hunt token not configured, skipping."

    url = "https://api.producthunt.com/v2/api/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    query = """
    {
      posts(order: VOTES, first: %d) {
        edges {
          node {
            name
            tagline
            url
            votesCount
          }
        }
      }
    }
    """ % limit

    resp = requests.post(url, json={"query": query}, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    posts = data.get("data", {}).get("posts", {}).get("edges", [])
    lines = []
    for edge in posts:
        node = edge["node"]
        lines.append(f"- {node['name']} - {node['tagline']} ({node['votesCount']} votes)\n  {node['url']}")

    return "\n".join(lines) if lines else "No trending products found."


# ---------- Lenny's Newsletter (RSS) ----------
def get_lennys_newsletter(limit=3):
    feed_url = "https://www.lennysnewsletter.com/feed"
    feed = feedparser.parse(feed_url)

    lines = []
    for entry in feed.entries[:limit]:
        title = entry.get("title", "No title")
        link = entry.get("link", "")
        lines.append(f"- {title}\n  {link}")

    return "\n".join(lines) if lines else "No recent posts found."


# ---------- Email ----------
def send_email(subject, body):
    sender = os.environ["MAIL_FROM"]
    password = os.environ["MAIL_PASSWORD"]
    receiver = os.environ["MAIL_TO"]

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)


def main():
    hn_section = get_hn_top_stories()
    ph_section = get_producthunt_trending()
    lenny_section = get_lennys_newsletter()

    body = f"""Weekly PM Digest

===== Hacker News - Top Stories =====
{hn_section}

===== Product Hunt - Trending =====
{ph_section}

===== Lenny's Newsletter - Latest Posts =====
{lenny_section}
"""

    send_email("Weekly PM Digest", body)


if __name__ == "__main__":
    main()
