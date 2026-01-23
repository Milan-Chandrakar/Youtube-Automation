"""
Analysis module for YouTube video data.
Performs sentiment analysis, NLP, trending analysis, and insights extraction.
"""

import logging
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
from collections import Counter
from config import (
    SENTIMENT_THRESHOLD_POSITIVE,
    SENTIMENT_THRESHOLD_NEGATIVE,
    MIN_ENGAGEMENT_THRESHOLD,
    CSV_EXPORT_PATH,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize NLP tools
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("Loaded spaCy model")
except OSError:
    logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

sentiment_analyzer = SentimentIntensityAnalyzer()


class YouTubeAnalyzer:
    """Analyzes YouTube video data for trends, sentiment, and insights."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.insights = {}

    def analyze_sentiment(self) -> pd.DataFrame:
        """
        Perform sentiment analysis on video titles and descriptions.

        Returns:
            DataFrame with sentiment scores
        """
        logger.info("Performing sentiment analysis")

        sentiments = []
        for idx, row in self.df.iterrows():
            text = f"{row['title']} {row['description']}"
            scores = sentiment_analyzer.polarity_scores(text)
            sentiments.append(
                {
                    "video_id": row["video_id"],
                    "compound_sentiment": scores["compound"],
                    "positive": scores["pos"],
                    "negative": scores["neg"],
                    "neutral": scores["neu"],
                }
            )

        sentiment_df = pd.DataFrame(sentiments)
        self.df = self.df.merge(sentiment_df, on="video_id")
        return self.df

    def extract_key_topics(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extract key topics/entities from text using spaCy.

        Args:
            text: Input text
            top_n: Number of top topics to return

        Returns:
            List of key topics
        """
        if nlp is None:
            return []

        doc = nlp(text)
        entities = [ent.text for ent in doc.ents if ent.label_ in ["PRODUCT", "ORG", "PERSON"]]
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]

        # Combine and get most common
        all_topics = entities + noun_phrases
        topic_counts = Counter(all_topics)
        return [topic for topic, _ in topic_counts.most_common(top_n)]

    def identify_trending_videos(self, top_n: int = 10) -> pd.DataFrame:
        """
        Identify trending videos based on engagement metrics.

        Args:
            top_n: Number of videos to return

        Returns:
            DataFrame of trending videos
        """
        logger.info("Identifying trending videos")

        # Calculate engagement score
        self.df["engagement_score"] = (
            self.df["view_count"] * 0.5
            + self.df["like_count"] * 2.0
            + self.df["comment_count"] * 3.0
        )

        # Filter by engagement threshold
        trending = self.df[
            self.df["comment_count"] >= MIN_ENGAGEMENT_THRESHOLD
        ].nlargest(top_n, "engagement_score")

        self.insights["trending_videos"] = trending[
            ["title", "channel_title", "view_count", "engagement_score"]
        ].to_dict("records")

        return trending

    def analyze_engagement(self) -> Dict:
        """
        Analyze engagement metrics across all videos.

        Returns:
            Dictionary with engagement statistics
        """
        logger.info("Analyzing engagement metrics")

        engagement_stats = {
            "avg_views": self.df["view_count"].mean(),
            "median_views": self.df["view_count"].median(),
            "avg_likes": self.df["like_count"].mean(),
            "avg_comments": self.df["comment_count"].mean(),
            "engagement_rate": (
                (self.df["like_count"] + self.df["comment_count"])
                / self.df["view_count"]
            ).mean(),
        }

        self.insights["engagement_stats"] = engagement_stats
        return engagement_stats

    def analyze_sentiment_distribution(self) -> Dict:
        """
        Analyze distribution of sentiment across videos.

        Returns:
            Dictionary with sentiment statistics
        """
        logger.info("Analyzing sentiment distribution")

        positive_count = (self.df["compound_sentiment"] > SENTIMENT_THRESHOLD_POSITIVE).sum()
        negative_count = (self.df["compound_sentiment"] < SENTIMENT_THRESHOLD_NEGATIVE).sum()
        neutral_count = len(self.df) - positive_count - negative_count

        sentiment_dist = {
            "positive": int(positive_count),
            "negative": int(negative_count),
            "neutral": int(neutral_count),
            "avg_sentiment": float(self.df["compound_sentiment"].mean()),
        }

        self.insights["sentiment_distribution"] = sentiment_dist
        return sentiment_dist

    def extract_industry_themes(self) -> Dict:
        """
        Extract major themes in the AI/automation space from video titles.

        Returns:
            Dictionary with theme analysis
        """
        logger.info("Extracting industry themes")

        all_titles = " ".join(self.df["title"].fillna(""))
        themes = self.extract_key_topics(all_titles, top_n=15)

        self.insights["industry_themes"] = {"top_themes": themes}
        return {"top_themes": themes}

    def get_channel_insights(self, top_n: int = 10) -> pd.DataFrame:
        """
        Analyze top performing channels.

        Args:
            top_n: Number of channels to return

        Returns:
            DataFrame with channel statistics
        """
        logger.info("Analyzing top channels")

        channel_stats = (
            self.df.groupby("channel_title")
            .agg(
                {
                    "video_id": "count",
                    "view_count": "sum",
                    "like_count": "sum",
                    "comment_count": "sum",
                }
            )
            .rename(
                columns={
                    "video_id": "video_count",
                    "view_count": "total_views",
                    "like_count": "total_likes",
                    "comment_count": "total_comments",
                }
            )
            .sort_values("total_views", ascending=False)
            .head(top_n)
        )

        self.insights["top_channels"] = channel_stats.to_dict("index")
        return channel_stats

    def run_full_analysis(self) -> Dict:
        """
        Run complete analysis pipeline.

        Returns:
            Dictionary with all insights
        """
        logger.info("Running full analysis pipeline")

        self.analyze_sentiment()
        self.identify_trending_videos()
        self.analyze_engagement()
        self.analyze_sentiment_distribution()
        self.extract_industry_themes()
        self.get_channel_insights()

        logger.info("Analysis complete")
        return self.insights


def main():
    """Example usage."""
    df = pd.read_csv(CSV_EXPORT_PATH)
    analyzer = YouTubeAnalyzer(df)
    insights = analyzer.run_full_analysis()

    print("\n=== Analysis Results ===")
    for key, value in insights.items():
        print(f"\n{key}:")
        print(value)


if __name__ == "__main__":
    main()
