"""
Email module for sending reports via Gmail.
Uses Gmail API for reliable delivery with attachments.
"""

import logging
import smtplib
from pathlib import Path
from typing import Dict
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from config import GMAIL_SENDER_EMAIL, GMAIL_APP_PASSWORD, GMAIL_RECIPIENT

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """Sends emails with attachments using Gmail SMTP."""

    def __init__(self, sender_email: str = GMAIL_SENDER_EMAIL, app_password: str = GMAIL_APP_PASSWORD):
        self.sender_email = sender_email
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_report(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        attachment_path: Path,
    ) -> bool:
        """
        Send email with report attachment.

        Args:
            recipient_email: Email address of recipient
            subject: Email subject
            body: Email body text
            attachment_path: Path to file to attach

        Returns:
            True if sent successfully, False otherwise
        """
        logger.info(f"Preparing email to {recipient_email}")

        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject

            # Add body
            message.attach(MIMEText(body, "plain"))

            # Add attachment
            if attachment_path.exists():
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {attachment_path.name}",
                )
                message.attach(part)
                logger.info(f"Attached file: {attachment_path.name}")
            else:
                logger.warning(f"Attachment file not found: {attachment_path}")

            # Send email
            logger.info(f"Connecting to {self.smtp_server}:{self.smtp_port}")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.send_message(message)

            logger.info(f"Email sent successfully to {recipient_email}")
            return True

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def send_report_batch(
        self,
        recipients: list,
        subject: str,
        body: str,
        attachment_path: Path,
    ) -> Dict[str, bool]:
        """
        Send report to multiple recipients.

        Args:
            recipients: List of email addresses
            subject: Email subject
            body: Email body
            attachment_path: Path to attachment

        Returns:
            Dictionary with send status for each recipient
        """
        results = {}
        for recipient in recipients:
            success = self.send_report(recipient, subject, body, attachment_path)
            results[recipient] = success

        return results


def main():
    """Example usage."""
    sender = EmailSender()

    report_path = Path("reports/YouTube_Trends_Report.pptx")

    body = """
Hello,

Please find attached your YouTube Trends Analysis Report.

This report includes:
- Executive summary of key metrics
- Sentiment analysis of trending videos
- Top performing channels
- Industry themes and recommendations

Best regards,
YouTube Automation System
    """

    success = sender.send_report(
        recipient_email=GMAIL_RECIPIENT,
        subject="YouTube Trends Report - AI & Automation",
        body=body,
        attachment_path=report_path,
    )

    if success:
        print("Report sent successfully!")
    else:
        print("Failed to send report")


if __name__ == "__main__":
    main()
