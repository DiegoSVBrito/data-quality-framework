import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_alert(suite_name: str, results: dict, recipients: list = None):
    recipients = recipients or os.getenv("DQ_ALERT_EMAILS", "").split(",")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")

    if not all([smtp_user, smtp_pass, recipients[0]]):
        print("Email not configured, skipping notification")
        return

    failed = [r for r in results["results"] if not r["success"]]
    failed_rows = "".join(
        f"<tr><td>{r['expectation']}</td><td>{r['kwargs']}</td></tr>"
        for r in failed
    )

    html = f"""
    <h2>Data Quality Report: {suite_name}</h2>
    <table border="1" cellpadding="5">
      <tr><th>Metric</th><th>Value</th></tr>
      <tr><td>Total</td><td>{results['total']}</td></tr>
      <tr><td>Passed</td><td>{results['passed']}</td></tr>
      <tr><td>Failed</td><td>{results['failed']}</td></tr>
      <tr><td>Success Rate</td><td>{results['success_rate']:.1f}%</td></tr>
    </table>
    <h3>Failed Expectations</h3>
    <table border="1" cellpadding="5">
      <tr><th>Expectation</th><th>Details</th></tr>
      {failed_rows}
    </table>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Data Quality Alert: {suite_name}"
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, recipients, msg.as_string())
