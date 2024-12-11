from flask import Flask, jsonify, request
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
CORS(app)

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    try:
        if 'youtu.be' in url:
            return url.split('/')[-1]
        
        parsed_url = urlparse(url)
        if parsed_url.hostname == 'www.youtube.com':
            return parse_qs(parsed_url.query)['v'][0]
        return url  # If it's already a video ID
    except:
        return None

@app.route('/transcript', methods=['GET'])
def get_transcript():
    # Get video URL or ID from query parameters
    video_input = request.args.get('videoId')
    language = request.args.get('language', 'en')  # Default to English if not specified
    
    if not video_input:
        return jsonify({'error': 'Video ID or URL is required'}), 400
    
    try:
        # Extract video ID if a URL was provided
        video_id = get_video_id(video_input)
        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL or video ID'}), 400

        # Fetch transcript
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        try:
            transcript = transcript_list.find_transcript([language])
        except:
            # If requested language not found, try to get auto-translated version
            try:
                transcript = transcript_list.find_transcript(['en']).translate(language)
            except:
                return jsonify({'error': f'No transcript available in {language}'}), 404
        
        transcript_data = transcript.fetch()
        
        # Return the full response with timing information
        return jsonify({
            'videoId': video_id,
            'language': language,
            'transcript': transcript_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3004, debug=True)