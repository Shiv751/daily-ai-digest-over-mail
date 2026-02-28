import os
import re
import smtplib
import anthropic
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ─── CONFIG ───────────────────────────────────────────────────────────────────
RECIPIENT_EMAIL   = os.environ["RECIPIENT_EMAIL"]    # Set in GitHub Secrets
SENDER_EMAIL      = os.environ["SENDER_EMAIL"]        # Your Gmail address
SENDER_PASSWORD   = os.environ["SENDER_PASSWORD"]     # Gmail App Password
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]   # From console.anthropic.com
# ──────────────────────────────────────────────────────────────────────────────

def fetch_ai_news_via_claude():
    today = datetime.now().strftime("%B %d, %Y")
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Today is {today}. Search the web and find the top 6 most important and latest "
                    f"AI news stories from around the world published today. "
                    f"For each story provide: a clear headline, the news source name, and a 2-3 sentence "
                    f"summary in short paragraph format. "
                    f"Format your response as a numbered list. Keep it factual and global in scope."
                )
            }
        ]
    )

    result = ""
    for block in response.content:
        if block.type == "text":
            result += block.text
    return result


def parse_into_html_items(raw_text):
    items = re.split(r'\n(?=\d+\.)', raw_text.strip())
    html = ""
    for item in items:
        item = item.strip()
        if not item:
            continue
        lines = item.split("\n", 1)
        headline = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        html += f"""
        <div style="margin-bottom:24px; padding:18px; background:#f9f9f9;
                    border-left:4px solid #4F46E5; border-radius:6px;">
            <h2 style="margin:0 0 10px; font-size:16px; color:#1a1a2e;">{headline}</h2>
            <p style="margin:0; font-size:14px; color:#444; line-height:1.7;">{body}</p>
        </div>
        """
    return html


def build_html(raw_text):
    today = datetime.now().strftime("%B %d, %Y")
    items_html = parse_into_html_items(raw_text)
    return f"""
    <html><body style="font-family:Arial,sans-serif; max-width:680px; margin:auto; color:#222;">
        <div style="background:#4F46E5; padding:24px 28px; border-radius:8px 8px 0 0;">
            <h1 style="color:#fff; margin:0; font-size:22px;">🤖 Daily AI News Digest</h1>
            <p style="color:#c7d2fe; margin:6px 0 0; font-size:14px;">
                {today} &bull; Top Stories in AI Globally &bull; Powered by Claude
            </p>
        </div>
        <div style="padding:24px 28px; border:1px solid #e5e7eb; border-top:none; border-radius:0 0 8px 8px;">
            {items_html}
            <hr style="border:none; border-top:1px solid #e5e7eb; margin:24px 0;">
            <p style="font-size:12px; color:#999; text-align:center;">
                Delivered daily at 10:00 AM IST &bull; Curated by Claude AI
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
    print("🔍 Fetching today's AI news via Claude...")
    raw_news = fetch_ai_news_via_claude()
    print("✍️  Building email...")
    html = build_html(raw_news)
    print("📧 Sending email...")
    send_email(html)
