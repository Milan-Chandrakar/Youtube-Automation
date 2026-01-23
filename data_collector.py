"""
Data collection module for YouTube videos and metadata.
Integrates YouTube API v3 and yt-dlp for comprehensive data gathering.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
import yt_dlp
import pandas as pd
from config import (
    YOUTUBE_API_KEY,
    SEARCH_QUERY,
    MAX_VIDEOS_PER_SEARCH,
    DAYS_BACK,
    CSV_EXPORT_PATH,
    TRANSCRIPTS_PATH,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YouTubeDataCollector:
    """Collects data from YouTube using official API and yt-dlp."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.videos_data = []

    def search_videos(
        self,
        query: str,
        max_results: int = MAX_VIDEOS_PER_SEARCH,
        days_back: int = DAYS_BACK,
    ) -> List[Dict]:
        """
        Search for videos on YouTube using the API.

        Args:
            query: Search query string
            max_results: Maximum number of results
            days_back: Only include videos from last N days

        Returns:
            List of video metadata dictionaries
        """
        logger.info(f"Searching YouTube for: {query}")

        # Calculate publish date filter
        published_after = (
            datetime.utcnow() - timedelta(days=days_back)
        ).isoformat() + "Z"

        params = {
            "q": query,
            "part": "snippet",
            "type": "video",
            "key": self.api_key,
            "maxResults": min(max_results, 50),  # API limit per request
            "publishedAfter": published_after,
            "order": "relevance",
        }

        try:
            response = requests.get(
                f"{self.base_url}/search", params=params, timeout=10
            )
            response.raise_for_status()
            results = response.json()

            video_ids = [item["id"]["videoId"] for item in results.get("items", [])]
            logger.info(f"Found {len(video_ids)} videos")

            # Get video statistics
            videos = self.get_video_statistics(video_ids)
            return videos

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return []

    def get_video_statistics(self, video_ids: List[str]) -> List[Dict]:
        """
        Retrieve statistics for specific videos.

        Args:
            video_ids: List of YouTube video IDs

        Returns:
            List of video data with statistics
        """
        videos = []
        batch_size = 50  # API allows max 50 per request

        for i in range(0, len(video_ids), batch_size):
            batch = video_ids[i : i + batch_size]
            params = {
                "id": ",".join(batch),
                "part": "statistics,snippet,contentDetails",
                "key": self.api_key,
            }

            try:
                response = requests.get(
                    f"{self.base_url}/videos", params=params, timeout=10
                )
                response.raise_for_status()
                items = response.json().get("items", [])

                for item in items:
                    video_data = self._parse_video_item(item)
                    videos.append(video_data)

            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to get statistics: {e}")

        return videos

    def _parse_video_item(self, item: Dict) -> Dict:
        """Parse a single video item from API response."""
        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})
        content_details = item.get("contentDetails", {})

        return {
            "video_id": item.get("id"),
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "channel_id": snippet.get("channelId"),
            "channel_title": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url"),
            "view_count": int(statistics.get("viewCount", 0)),
            "like_count": int(statistics.get("likeCount", 0)),
            "comment_count": int(statistics.get("commentCount", 0)),
            "duration": content_details.get("duration"),
            "collected_at": datetime.utcnow().isoformat(),
        }

    def get_video_transcript(self, video_id: str) -> Optional[str]:
        """
        Extract transcript/captions from a video.

        Args:
            video_id: YouTube video ID

        Returns:
            Full transcript text or None if unavailable
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([item["text"] for item in transcript])
            return full_text
        except TranscriptsDisabled:
            logger.warning(f"Transcripts disabled for video {video_id}")
            return None
        except Exception as e:
            logger.warning(f"Could not get transcript for {video_id}: {e}")
            return None

    def collect_full_data(self, query: str = SEARCH_QUERY) -> pd.DataFrame:
        """
        Complete data collection pipeline.

        Args:
            query: Search query

        Returns:
            DataFrame with collected video data
        """
        logger.info("Starting full data collection pipeline")

        # Search and get video statistics
        videos = self.search_videos(query)
        logger.info(f"Collected statistics for {len(videos)} videos")

        # Get transcripts for each video
        for video in videos:
            video_id = video["video_id"]
            transcript = self.get_video_transcript(video_id)
            video["transcript"] = transcript

            if transcript:
                transcript_path = TRANSCRIPTS_PATH / f"{video_id}.txt"
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(transcript)
                logger.info(f"Saved transcript for {video_id}")

        # Convert to DataFrame
        df = pd.DataFrame(videos)
        df.to_csv(CSV_EXPORT_PATH, index=False)
        logger.info(f"Exported {len(df)} videos to {CSV_EXPORT_PATH}")

        return df


def main():
    """Example usage."""
    collector = YouTubeDataCollector(YOUTUBE_API_KEY)
    df = collector.collect_full_data()
    print(f"Collected {len(df)} videos")
    print(df.head())


if __name__ == "__main__":
    main()
