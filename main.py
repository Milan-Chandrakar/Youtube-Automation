"""
Main orchestration module for YouTube automation system.
Coordinates data collection, analysis, report generation, and email delivery.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

from config import YOUTUBE_API_KEY, GMAIL_RECIPIENT, REPORT_TITLE, CSV_EXPORT_PATH, SEARCH_QUERY
from data_collector import YouTubeDataCollector
from analyzer import YouTubeAnalyzer
from report_generator import ReportGenerator
from email_sender import EmailSender

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class YouTubeAutomationPipeline:
    """Main pipeline for YouTube data collection, analysis, and reporting."""

    def __init__(self):
        self.collector = YouTubeDataCollector(YOUTUBE_API_KEY)
        self.analyzer = None
        self.df = None
        self.insights = None
        self.report_path = None

    def step1_collect_data(self, query: str = None) -> bool:
        """
        Step 1: Collect data from YouTube.

        Args:
            query: Search query for YouTube (defaults to SEARCH_QUERY from config)

        Returns:
            True if successful
        """
        if query is None:
            query = SEARCH_QUERY
        logger.info("=" * 60)
        logger.info("STEP 1: Collecting YouTube Data")
        logger.info("=" * 60)

        try:
            self.df = self.collector.collect_full_data(query)
            logger.info(f"✓ Successfully collected data for {len(self.df)} videos")
            return True
        except Exception as e:
            logger.error(f"✗ Data collection failed: {e}")
            return False

    def step2_analyze_data(self) -> bool:
        """
        Step 2: Analyze collected data.

        Returns:
            True if successful
        """
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: Analyzing Data")
        logger.info("=" * 60)

        try:
            if self.df is None or len(self.df) == 0:
                logger.error("No data available for analysis")
                return False

            self.analyzer = YouTubeAnalyzer(self.df)
            self.insights = self.analyzer.run_full_analysis()
            self.df = self.analyzer.df  # Update df with analysis results
            logger.info("✓ Analysis complete")
            return True
        except Exception as e:
            logger.error(f"✗ Analysis failed: {e}")
            return False

    def step3_generate_report(self) -> bool:
        """
        Step 3: Generate presentation report.

        Returns:
            True if successful
        """
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: Generating Report")
        logger.info("=" * 60)

        try:
            if self.insights is None:
                logger.error("No insights available for report generation")
                return False

            generator = ReportGenerator(self.insights, self.df)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"YouTube_Trends_Report_{timestamp}.pptx"
            self.report_path = generator.generate_presentation(filename)
            logger.info(f"✓ Report generated: {self.report_path}")
            return True
        except Exception as e:
            logger.error(f"✗ Report generation failed: {e}")
            return False

    def step4_send_email(self, recipient: str = GMAIL_RECIPIENT, send_email: bool = True) -> bool:
        """
        Step 4: Send report via email.

        Args:
            recipient: Email recipient address
            send_email: Whether to actually send (default True)

        Returns:
            True if successful or skipped
        """
        logger.info("\n" + "=" * 60)
        logger.info("STEP 4: Sending Report via Email")
        logger.info("=" * 60)

        if not send_email:
            logger.info("⊘ Email sending skipped (disabled)")
            return True

        try:
            if self.report_path is None:
                logger.error("No report available to send")
                return False

            sender = EmailSender()

            body = f"""
Hello,

Please find attached your YouTube Trends Analysis Report for the AI & Automation niche.

Report Details:
- Videos Analyzed: {len(self.df)}
- Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Time Period: Last 30 days

Key Findings:
- Average Views per Video: {self.insights.get('engagement_stats', {}).get('avg_views', 0):,.0f}
- Engagement Rate: {self.insights.get('engagement_stats', {}).get('engagement_rate', 0):.2%}
- Positive Sentiment Videos: {self.insights.get('sentiment_distribution', {}).get('positive', 0)}
- Top Themes: {', '.join(self.insights.get('industry_themes', {}).get('top_themes', [])[:5])}

This report includes:
✓ Executive Summary
✓ Engagement Analysis
✓ Sentiment Distribution
✓ Industry Trends
✓ Top Performing Channels
✓ Actionable Recommendations

Best regards,
YouTube Automation System
            """

            success = sender.send_report(
                recipient_email=recipient,
                subject=f"{REPORT_TITLE} - {datetime.now().strftime('%B %d, %Y')}",
                body=body,
                attachment_path=self.report_path,
            )

            if success:
                logger.info(f"✓ Email sent successfully to {recipient}")
                return True
            else:
                logger.error("✗ Failed to send email")
                return False

        except Exception as e:
            logger.error(f"✗ Email sending failed: {e}")
            return False

    def run_full_pipeline(self, send_email: bool = True, query: str = None) -> bool:
        """
        Run complete automation pipeline.

        Args:
            send_email: Whether to send report via email
            query: YouTube search query (defaults to SEARCH_QUERY from config)

        Returns:
            True if all steps successful
        """
        logger.info("\n" + "=" * 80)
        logger.info("YOUTUBE AUTOMATION PIPELINE STARTING")
        logger.info("=" * 80)

        if query is None:
            query = SEARCH_QUERY

        steps = [
            ("Data Collection", lambda: self.step1_collect_data(query)),
            ("Data Analysis", lambda: self.step2_analyze_data()),
            ("Report Generation", lambda: self.step3_generate_report()),
            ("Email Delivery", lambda: self.step4_send_email(send_email=send_email)),
        ]

        results = {}
        for step_name, step_func in steps:
            try:
                success = step_func()
                results[step_name] = "✓ PASSED" if success else "✗ FAILED"
                if not success:
                    logger.warning(f"Pipeline halted at: {step_name}")
                    break
            except Exception as e:
                logger.error(f"Unexpected error in {step_name}: {e}")
                results[step_name] = "✗ ERROR"
                break

        # Print summary
        logger.info("\n" + "=" * 80)
        logger.info("PIPELINE EXECUTION SUMMARY")
        logger.info("=" * 80)
        for step, result in results.items():
            logger.info(f"{step}: {result}")
        logger.info("=" * 80)

        return all("✓" in r for r in results.values())


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="YouTube Automation Pipeline")
    parser.add_argument(
        "--query",
        type=str,
        default=SEARCH_QUERY,
        help="YouTube search query",
    )
    parser.add_argument(
        "--skip-email",
        action="store_true",
        help="Skip email sending",
    )
    parser.add_argument(
        "--recipient",
        type=str,
        default=GMAIL_RECIPIENT,
        help="Email recipient address",
    )

    args = parser.parse_args()

    pipeline = YouTubeAutomationPipeline()
    success = pipeline.run_full_pipeline(send_email=not args.skip_email, query=args.query)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
