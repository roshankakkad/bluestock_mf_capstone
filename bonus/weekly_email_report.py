"""B5 - Automated HTML email report generator for weekly summaries.

Configure SMTP credentials through environment variables before sending.
"""
from email.mime.text import MIMEText
from pathlib import Path
import os
import smtplib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def build_html_report() -> str:
    scorecard = pd.read_csv(PROCESSED / "fund_scorecard.csv").head(10)
    return "<h2>Bluestock MF Weekly Performance Summary</h2>" + scorecard.to_html(index=False)


def send_report(to_email: str) -> None:
    msg = MIMEText(build_html_report(), "html")
    msg["Subject"] = "Bluestock MF Weekly Performance Summary"
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = to_email
    with smtplib.SMTP_SSL(os.environ.get("SMTP_HOST", "smtp.gmail.com"), int(os.environ.get("SMTP_PORT", "465"))) as server:
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        server.send_message(msg)
