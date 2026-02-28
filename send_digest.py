import os
import smtplib
import requests
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ─── CONFIG ───────────────────────────────────────────────────────────────────
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]   # Set in GitHub Secrets
SENDER_EMAIL    = os.environ["SENDER_EMAIL"]       # Your Gmail address
SENDER_PASSWORD = os.environ["SENDER_PASSWORD"]    # Gmail App Password
NEWS_API_KEY    = os.environ["NEWS_API_KEY"]        # From newsapi.org
# ──────────────────────────────────────────────────────────────────────────────

def fetch_ai_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "artificial intelligence OR AI technology",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 8,
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("articles", [])

def build_html(articles):
    today = datetime.now().strftime("%B %d, %Y")
    items_html = ""
    for i, article in enumerate(articles, 1):
        title       = article.get("title", "No Title")
        description = article.get("description") or "No summary available."
        source      = article.get("source", {}).get("name", "Unknown Source")
        url         = article.get("url", "#")
        published   = article.get("publishedAt", "")[:10]

        items_html += f"""
        <div style="margin-bottom:28px; padding:18px; background:#f9f9f9;
                    border-left:4px solid #4F46E5; border-radius:6px;">
            <p style="margin:0 0 4px; font-size:13px; color:#888;">{i}. {source} &bull; {published}</p>
            <h2 style="margin:0 0 10px; font-size:17px; color:#1a1a2e;">
                <a href="{url}" style="color:#4F46E5; text-decoration:none;">{title}</a>
            </h2>
            <p style="margin:0; font-size:14px; color:#444; line-height:1.6;">{description}</p>
        </div>
        """

    return f"""
    <html><body style="font-family:Arial,sans-serif; max-width:680px; margin:auto; color:#222;">
        <div style="background:#4F46E5; padding:24px 28px; border-radius:8px 8px 0 0;">
            <h1 style="color:#fff; margin:0; font-size:22px;">🤖 Daily AI News Digest</h1>
            <p style="color:#c7d2fe; margin:6px 0 0; font-size:14px;">{today} &bull; Top Stories in AI Globally</p>
        </div>
        <div style="padding:24px 28px; border:1px solid #e5e7eb; border-top:none; border-radius:0 0 8px 8px;">
            {items_html}
            <hr style="border:none; border-top:1px solid #e5e7eb; margin:24px 0;">
            <p style="font-size:12px; color:#999; text-align:center;">
                Delivered daily at 10:00 AM IST &bull; Powered by NewsAPI &bull; Curated for you
            </p>
        </div>
    </body></html>
    """

def send_email(html_content):
    today = datetime.now().strftime("%B %d, %Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🤖 AI Daily Digest – {today}"
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = RECIPIENT_EMAIL
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    print(f"✅ Digest sent to {RECIPIENT_EMAIL}")

if __name__ == "__main__":
    articles = fetch_ai_news()
    html     = build_html(articles)
    send_email(html)
