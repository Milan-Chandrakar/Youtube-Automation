# YouTube Automation System

An intelligent automation system that scrapes YouTube videos in the AI & AI Automation niche, analyzes trends and sentiment, and generates professional slide deck reports.

## Features

✅ **Automated Data Collection**
- YouTube Data API v3 integration for video metadata and statistics
- Transcript extraction using youtube-transcript-api
- Comprehensive data storage in SQLite and CSV formats

✅ **Advanced Analysis**
- Sentiment analysis using VADER (optimized for social media)
- NLP-powered topic extraction using spaCy
- Engagement metrics calculation
- Trending video identification
- Channel performance analysis

✅ **Professional Reporting**
- Automated presentation generation with python-pptx
- Interactive visualizations using Plotly
- Executive summaries and key takeaways
- Industry trends and recommendations

✅ **Automated Delivery**
- Gmail API integration for reliable email delivery
- Scheduled report sending
- Professional formatting with attachments

## Installation

### Prerequisites
- Python 3.8+
- YouTube Data API key
- Gmail App Password (for email functionality)

### Setup

1. **Clone and navigate to project:**
```bash
cd youtube_automation
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Download spaCy model:**
```bash
python -m spacy download en_core_web_sm
```

4. **Configure credentials:**

Create a `.env` file in the project root:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
GMAIL_SENDER_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
GMAIL_RECIPIENT=recipient@example.com
```

Or set environment variables:
```bash
export YOUTUBE_API_KEY="your_key"
export GMAIL_SENDER_EMAIL="your_email"
export GMAIL_APP_PASSWORD="your_password"
export GMAIL_RECIPIENT="recipient_email"
```

## Getting API Credentials

### YouTube Data API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (API key)
5. Copy the key to config or environment variable

### Gmail App Password
1. Enable 2-Factor Authentication on Google Account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Select "Mail" and "Windows Computer"
4. Generate and copy the app password

## Usage

### Run Full Pipeline
```bash
python main.py
```

### Run with Custom Query
```bash
python main.py --query "machine learning tutorials"
```

### Skip Email Sending
```bash
python main.py --skip-email
```

### Run Individual Modules

**Collect Data Only:**
```bash
python data_collector.py
```

**Analyze Data:**
```bash
python analyzer.py
```

**Generate Report:**
```bash
python report_generator.py
```

**Send Email:**
```bash
python email_sender.py
```

## Project Structure

```
youtube_automation/
├── config.py                 # Configuration and settings
├── data_collector.py         # YouTube API and data collection
├── analyzer.py               # Analysis (sentiment, NLP, trends)
├── report_generator.py       # Presentation generation
├── email_sender.py           # Email delivery
├── main.py                   # Pipeline orchestration
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── data/                     # Collected data
│   ├── youtube_data.db       # SQLite database
│   ├── videos.csv            # Video metadata CSV
│   └── transcripts/          # Video transcripts
├── reports/                  # Generated reports
│   └── charts/               # Visualization images
└── logs/                     # Application logs
```

## Configuration

Edit `config.py` to customize:

- **Search parameters:** Query, time range, max results
- **Analysis thresholds:** Sentiment cutoffs, engagement minimums
- **Report settings:** Title, output paths, recipient
- **API limits:** YouTube quota configuration

## Data Outputs

### CSV Format
`data/videos.csv` contains:
- Video ID, Title, Description
- Channel info (ID, title, subscriber count)
- Engagement metrics (views, likes, comments)
- Published date, duration
- Sentiment scores
- Transcripts (stored separately)

### Database
SQLite database in `data/youtube_data.db` for efficient querying and updates.

### Reports
Generated PowerPoint presentations include:
- Title slide with metadata
- Executive summary
- Engagement analysis charts
- Sentiment distribution pie charts
- Industry themes and trending topics
- Top performing channels
- Actionable recommendations

## Analysis Capabilities

### Sentiment Analysis
- **VADER Sentiment Analyzer:** Optimized for social media and casual text
- Classifies as: Positive, Negative, or Neutral
- Handles slang, emojis, and intensity modifiers

### NLP Analysis
- **Entity Recognition:** Identifies companies, products, people
- **Noun Phrases:** Extracts key terms and concepts
- **Topic Clustering:** Identifies major themes

### Engagement Metrics
- View counts, like counts, comment counts
- Engagement rate calculation
- Trending score computation
- Channel performance analytics

## Troubleshooting

### "API quota exceeded"
- YouTube API has daily quota limits
- Reduce `MAX_VIDEOS_PER_SEARCH` in config.py
- Run less frequently or optimize API calls

### "Transcripts disabled"
- Some videos don't have transcripts available
- System logs warnings and continues with other videos

### "Gmail authentication failed"
- Verify app password (not regular password)
- Check 2-Factor Authentication is enabled
- Ensure credentials are correctly set

### "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

## Performance Tips

1. **Cache data:** Reuse previously collected data when possible
2. **Batch processing:** Collect data in batches to manage API quotas
3. **Scheduled runs:** Use system scheduler (cron/Task Scheduler) for automation
4. **Database indexing:** Use SQL indexes for large datasets

## Extending the System

### Add custom analysis:
1. Extend `YouTubeAnalyzer` class
2. Add method to `run_full_analysis()`
3. Update report generator to display results

### Add more visualizations:
1. Create new chart functions in `report_generator.py`
2. Use Plotly for interactive charts
3. Export as PNG/SVG for embedding in slides

### Custom report templates:
1. Modify slide layouts in `ReportGenerator`
2. Use python-pptx for custom positioning
3. Add company branding/logos

## Scheduling Automation

### Linux/Mac (Cron)
```bash
# Run daily at 8 AM
0 8 * * * cd /path/to/youtube_automation && python main.py
```

### Windows (Task Scheduler)
1. Create task that runs: `python C:\path\to\youtube_automation\main.py`
2. Set trigger to desired schedule

## API Costs

- **YouTube Data API:** Free tier includes 10,000 units/day
- **Gmail API:** Free
- **No cost** for Plotly or python-pptx

## License

MIT License - Feel free to modify and distribute

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review error messages in config setup
3. Verify API credentials and permissions
4. Check internet connectivity

## Future Enhancements

- [ ] Advanced ML for topic modeling
- [ ] Real-time trend detection
- [ ] Competitor analysis
- [ ] Content recommendation engine
- [ ] Dashboard for visualization
- [ ] Multi-language support
- [ ] Video download and analysis
- [ ] Comment sentiment analysis
- [ ] Influencer identification
