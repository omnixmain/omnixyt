from flask import Flask, redirect, request, jsonify
import yt_dlp

app = Flask(__name__)

# Basic ytdl options for fast extraction
YDL_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'skip_download': True,
    'format': 'best',
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web']
        }
    }
}

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "ytomnix API is running!",
        "usage": "/omnixyt/live/<video_id>"
    })

@app.route('/omnixyt/live/<video_id>')
def get_stream(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            # extract_info with download=False gets the metadata
            info = ydl.extract_info(url, download=False)
            
            # Check for live stream master manifest first
            if info.get('is_live'):
                stream_url = info.get('manifest_url')
                if not stream_url:
                    stream_url = info.get('url')
            else:
                # If it's a VOD (not live), just get the best url
                stream_url = info.get('url')
                
            if stream_url:
                # Redirect the player directly to the stream URL
                return redirect(stream_url, code=302)
            else:
                return jsonify({"error": "Stream URL not found"}), 404
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run locally on port 5000
    app.run(host='0.0.0.0', port=5000)
