"""
hr_emailer.py — Sends welcome emails to new hires.

Two operating modes:
  • Log-only (default):   If SMTP credentials are missing, prints what WOULD
                          be sent. Perfect for testing without any setup.
  • Live:                 If credentials are set in .env, actually sends.
"""
from __future__ import annotations

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

log = logging.getLogger("hr.emailer")


# --------------------------------------------------------------------------- #
# Config (all read from .env at import time)
# --------------------------------------------------------------------------- #
SMTP_HOST      = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT      = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER      = os.getenv("SMTP_USER", "").strip()
SMTP_PASS      = os.getenv("SMTP_PASS", "").strip()
SMTP_FROM      = os.getenv("SMTP_FROM", SMTP_USER).strip()
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "HR Team").strip()

COMPANY_NAME     = os.getenv("COMPANY_NAME", "Our Company").strip()
HR_CONTACT_EMAIL = os.getenv("HR_CONTACT_EMAIL", SMTP_FROM).strip()


# --------------------------------------------------------------------------- #
# Email builder
# --------------------------------------------------------------------------- #
def _build_welcome_email(
    first_name: str,
    job_title: str,
    department: str,
    start_date: str,
    hr_contact_email: str,
) -> tuple[str, str, str]:
    """Return (subject, html_body, plain_text_body)."""

    subject = f"Welcome to {COMPANY_NAME}!"

    plain = f"""Hi {first_name},

Welcome to {COMPANY_NAME}! We're thrilled to have you joining us as
{job_title} in the {department} team.

Start date: {start_date}

WHAT TO EXPECT ON YOUR FIRST DAY
  • Arrive at 9:00 AM (or your confirmed start time)
  • Bring a valid photo ID for building access
  • Your manager will meet you at reception
  • Your onboarding buddy will guide you through week one

BEFORE YOU START
  • Complete the attached new-hire paperwork
  • Reply to this email if you have any questions
  • Save our HR contact for emergencies

HR CONTACT
  Email: {hr_contact_email}

We can't wait to see you on {start_date}. Welcome aboard!

— The {COMPANY_NAME} Team
"""

    html = f"""\
<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; color: #222; max-width: 600px; margin: 0 auto; padding: 24px;">

  <h1 style="color: #2c3e50; font-size: 24px;">🎉 Welcome to {COMPANY_NAME}, {first_name}!</h1>

  <p style="font-size: 16px; line-height: 1.6;">
    We're thrilled to have you joining us as <strong>{job_title}</strong>
    in the <strong>{department}</strong> team.
  </p>

  <p style="font-size: 16px; padding: 12px 16px; background: #f0f7ff; border-left: 4px solid #3498db; border-radius: 4px;">
    <strong>Your start date:</strong> {start_date}
  </p>

  <h2 style="color: #2c3e50; font-size: 18px; margin-top: 32px;">What to expect on your first day</h2>
  <ul style="font-size: 15px; line-height: 1.8;">
    <li>Arrive at <strong>9:00 AM</strong> (or your confirmed start time)</li>
    <li>Bring a valid photo ID for building access</li>
    <li>Your manager will meet you at reception</li>
    <li>Your onboarding buddy will guide you through week one</li>
  </ul>

  <h2 style="color: #2c3e50; font-size: 18px; margin-top: 32px;">Before you start</h2>
  <ul style="font-size: 15px; line-height: 1.8;">
    <li>Complete the attached new-hire paperwork</li>
    <li>Reply to this email if you have any questions</li>
    <li>Save our HR contact for emergencies</li>
  </ul>

  <h2 style="color: #2c3e50; font-size: 18px; margin-top: 32px;">HR contact</h2>
  <p style="font-size: 15px;">
    📧 <a href="mailto:{hr_contact_email}" style="color: #3498db;">{hr_contact_email}</a>
  </p>

  <p style="font-size: 16px; margin-top: 32px;">
    We can't wait to see you on <strong>{start_date}</strong>. Welcome aboard!
  </p>

  <p style="color: #888; font-size: 14px; margin-top: 40px; border-top: 1px solid #eee; padding-top: 16px;">
    — The {COMPANY_NAME} Team
  </p>

</body>
</html>
"""

    return subject, html, plain


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def send_welcome_email(
    to_email: str,
    first_name: str,
    full_name: str,
    job_title: str,
    department: str,
    start_date: str,
) -> bool:
    """
    Send the welcome email. Returns True if sent (or logged in dry-run),
    False if it hard-failed.
    """
    if not to_email or "@" not in to_email:
        log.warning("No valid personal email — skipping welcome email for %s", full_name)
        return False

    subject, html, plain = _build_welcome_email(
        first_name=first_name,
        job_title=job_title,
        department=department,
        start_date=start_date,
        hr_contact_email=HR_CONTACT_EMAIL,
    )

    # Dry-run mode: no SMTP credentials, just log
    if not SMTP_HOST or not SMTP_USER:
        log.info("─" * 60)
        log.info("📧  WELCOME EMAIL (dry-run — no SMTP configured)")
        log.info("    To:      %s", to_email)
        log.info("    Subject: %s", subject)
        log.info("    Body preview:")
        for line in plain.splitlines()[:8]:
            log.info("      %s", line)
        log.info("    (Add SMTP_HOST, SMTP_USER, SMTP_PASS to .env to send for real)")
        log.info("─" * 60)
        return True

    # Live send
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"{SMTP_FROM_NAME} <{SMTP_FROM}>"
        msg["To"]      = to_email

        msg.attach(MIMEText(plain, "plain", "utf-8"))
        msg.attach(MIMEText(html,  "html",  "utf-8"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)

        log.info("📧  Welcome email SENT → %s", to_email)
        return True
    except Exception:
        log.exception("Failed to send welcome email to %s", to_email)
        return False