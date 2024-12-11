from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """
    Extract video ID from YouTube URL
    Works with both full URLs and shortened youtu.be links
    """
    if 'youtu.be' in url:
        return url.split('/')[-1]
    
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'www.youtube.com':
        return parse_qs(parsed_url.query)['v'][0]
    return url  # If it's already a video ID

def fetch_transcript(video_url, language='en'):
    """
    Fetch transcript for a YouTube video
    Args:
        video_url: YouTube video URL or video ID
        language: Language code (default: 'en' for English)
    Returns:
        Transcript text as a string
    """
    try:
        video_id = get_video_id(video_url)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        try:
            transcript = transcript_list.find_transcript([language])
        except:
            # If requested language not found, try to get auto-translated version
            transcript = transcript_list.find_transcript(['en']).translate(language)
        
        transcript_data = transcript.fetch()
        
        # Combine all text entries
        full_transcript = ' '.join([entry['text'] for entry in transcript_data])
        return full_transcript
    
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

if __name__ == "__main__":
    # Example usage
    video_url = input("Enter YouTube video URL: ")
    language = input("Enter language code (e.g., 'en' for English, press Enter for default): ").strip() or 'en'
    
    transcript = fetch_transcript(video_url, language)
    print("\nTranscript:")
    print(transcript)