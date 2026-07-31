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
            'player_client': ['ios', 'web']
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
            info = ydl.extract_info(url, download=False)
            
            if info.get('is_live'):
                stream_url = info.get('manifest_url') or info.get('url')
            else:
                stream_url = info.get('url')
                
            if stream_url:
                return redirect(stream_url, code=302)
            else:
                return jsonify({"error": "Stream URL not found"}), 404
                
    except Exception as e:
        error_msg = str(e)
        # If Vercel IP gets blocked by YouTube bot detection, fallback to a public API
        if "confirm you're not a bot" in error_msg.lower():
            # Fallback to a reliable Piped proxy to get the stream JSON
            import requests
            try:
                # Try fetching from piped API
                resp = requests.get(f"https://pipedapi.kavin.rocks/streams/{video_id}", timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("hls"):
                        return redirect(data["hls"], code=302)
            except:
                pass
            
            # If all else fails, redirect to a public proxy player
            return redirect(f"https://youtube.m3u8.tv/{video_id}", code=302)
            
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
