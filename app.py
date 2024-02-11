from googleapiclient.discovery import build
import os
from flask import request
#Transformers provides APIs and tools
# to easily download and train state-of-the-art pretrained models
from transformers import pipeline, BartForConditionalGeneration, BartTokenizer
#Conditional data generation -> where a generative model is asked to generate data
#according to some pre-specified conditioning, such as a topic, sentiment, text, or image-based dataset.

from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv  #To keep sensistive urls(api-keys,db urls) in .env file and loading them here to aoid hardcoding
load_dotenv()
from flask import Flask,jsonify
# Access the YouTube API key
API_KEY = os.environ.get("YOUTUBE_API_KEY")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
app = Flask(__name__)

  
def get_details(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)   #build func is used for creating a service obj "youtube" that is used for making api requests
    request = youtube.videos().list(part='snippet,statistics', id=video_id)
    response = request.execute()
    return response


#Specify the model and tokenizer for summarization
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

# Load the summarization pipeline with the specified model
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

def summarize_text(text):
    # Use the model to summarize the text
    summary_obj = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary_obj[0]['summary_text']





@app.route('/video-details')  # Updated route


def get_video_details():
    video_id = request.args.get("video_id")

    try:
        # Assuming you have a function get_details that fetches video details
        details = get_details(video_id)

        # Extract title and view count from the details
        title = details['items'][0]['snippet']['title']
        view_count = details['items'][0]['statistics']['viewCount']

        return jsonify({'title': title, 'viewCount': view_count})

    except Exception as e:
        # Handle the exception and return an error response
        return jsonify({'error': f'Error fetching video details: {str(e)}'})

    
@app.route('/summary-details')
def get_summary_details():
    video_id = str(request.args.get("video_id"))
    app.logger.info(f"Attempting to fetch summary for video_id: {video_id}")
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([item['text'] for item in transcript_list])
        # Truncate the transcript text to a specified maximum length (e.g., 512 characters)
        max_length = 512
        transcript_text = transcript_text[:max_length]
        summary = summarize_text(transcript_text)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': f'Error generating summary: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)