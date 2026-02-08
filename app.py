"""
Gradio web interface for YouTube Automation System.
Deployed on Hugging Face Spaces.
"""

import gradio as gr
import logging
import os
from datetime import datetime
from pathlib import Path
from main import YouTubeAutomationPipeline

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for required API keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def validate_api_keys():
    """Validate that required API keys are configured."""
    if not YOUTUBE_API_KEY:
        return False, "❌ YouTube API Key not configured. Please set YOUTUBE_API_KEY secret."
    return True, "✅ API keys configured"

def run_youtube_automation(search_query: str, send_email: bool = False) -> str:
    """
    Execute the YouTube automation pipeline.
    
    Args:
        search_query: YouTube search query
        send_email: Whether to send the report via email
        
    Returns:
        Status message with results
    """
    # Validate API keys
    keys_valid, key_msg = validate_api_keys()
    if not keys_valid:
        return key_msg
    
    if not search_query or search_query.strip() == "":
        return "❌ Error: Please enter a search query"
    
    try:
        logger.info(f"Starting automation pipeline for query: {search_query}")
        
        # Initialize pipeline
        pipeline = YouTubeAutomationPipeline()
        
        # Step 1: Collect data
        if not pipeline.step1_collect_data(search_query):
            return f"❌ Data collection failed"
        
        if pipeline.df is None or len(pipeline.df) == 0:
            return f"❌ No videos found for query: '{search_query}'"
        
        videos_collected = len(pipeline.df)
        
        # Step 2: Analyze data
        if not pipeline.step2_analyze_data():
            return f"❌ Analysis failed"
        
        # Step 3: Generate report
        if not pipeline.step3_generate_report():
            return f"❌ Report generation failed"
        
        # Step 4: Send email (optional)
        email_status = ""
        if send_email:
            if not GMAIL_APP_PASSWORD:
                email_status = "\n⚠️  Email not sent: GMAIL_APP_PASSWORD secret not configured"
            else:
                if pipeline.step4_send_email():
                    email_status = "\n✅ Report sent via email"
                else:
                    email_status = "\n⚠️  Report generated but email delivery failed"
        
        # Format success message
        report_link = f"📄 Report: {pipeline.report_path}" if pipeline.report_path else "📄 Report generated"
        
        result = f"""
✅ **YouTube Automation Completed Successfully!**

📊 **Results:**
- Videos Analyzed: {videos_collected}
- Analysis Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{report_link}{email_status}

**Next Steps:**
1. Download the report from the outputs folder
2. Review the analysis and insights
3. Use the data for decision-making
"""
        return result
        
    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}", exc_info=True)
        return f"❌ **Error:** {str(e)}\n\nPlease check the logs and try again."


# Create Gradio interface
with gr.Blocks(title="YouTube Automation", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎬 YouTube Automation System
    
    Automatically collect, analyze, and report on YouTube videos in your niche.
    
    **Features:**
    - ✅ Automated data collection from YouTube
    - ✅ Sentiment & trend analysis
    - ✅ Professional report generation
    - ✅ Email delivery (optional)
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Configuration")
            
            # API Key status
            api_status, status_msg = validate_api_keys()
            status_color = "🟢" if api_status else "🔴"
            gr.Markdown(f"**API Status:** {status_color} {status_msg}")
            
            gr.Markdown("---")
            
            # Input fields
            search_query = gr.Textbox(
                label="YouTube Search Query",
                placeholder="e.g., AI automation, machine learning trends, etc.",
                lines=2,
                value="AI automation"
            )
            
            send_email = gr.Checkbox(
                label="Send Report via Email?",
                value=False,
                info="Requires GMAIL_APP_PASSWORD to be configured"
            )
            
            run_button = gr.Button("🚀 Run Analysis", variant="primary", scale=2)
        
        with gr.Column():
            gr.Markdown("### Output")
            output = gr.Markdown()
    
    # Set button click handler
    run_button.click(
        fn=run_youtube_automation,
        inputs=[search_query, send_email],
        outputs=output,
        api_name="analyze"
    )
    
    gr.Markdown("""
    ---
    
    ### 📋 How to Use
    
    1. **Enter a search query** - What topics would you like to analyze?
    2. **Click "Run Analysis"** - The system will collect and analyze data
    3. **Download the report** - Check the outputs folder for your PowerPoint report
    4. **(Optional) Enable email** - Get the report sent to your inbox
    
    ### ⚙️ Required Secrets
    
    Set these in your Hugging Face Space settings:
    - `YOUTUBE_API_KEY` - Your YouTube Data API v3 key
    - `GMAIL_APP_PASSWORD` - (Optional) Gmail app password for email delivery
    - `GMAIL_RECIPIENT` - (Optional) Email recipient address
    
    ### 📚 Resources
    
    - [Get YouTube API Key](https://developers.google.com/youtube/registering_an_application)
    - [Gmail App Password Setup](https://support.google.com/accounts/answer/185833)
    """)


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
