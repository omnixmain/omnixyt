# YtOmnix - YouTube to M3U8 API

This is a lightweight Python Flask API that extracts the raw `.m3u8` stream from any YouTube video or live stream and redirects the player to it.

## How it works
If you request `https://your-api.vercel.app/omnixyt/live/<VIDEO_ID>`, the server will:
1. Fetch the raw stream URL using `yt-dlp`.
2. Return a `302 Redirect` to the actual YouTube server containing the stream.
3. Your IPTV Player / VLC will automatically follow the redirect and play the stream.

## How to Deploy for FREE on Vercel

1. **Upload to GitHub:**
   - Create a new repository on your GitHub account (e.g., `ytomnix-api`).
   - Upload all files from this folder (`app.py`, `requirements.txt`, `vercel.json`) to that repository.

2. **Deploy to Vercel:**
   - Go to [Vercel.com](https://vercel.com/) and log in with your GitHub account.
   - Click **"Add New..."** -> **"Project"**.
   - Import your `ytomnix-api` repository.
   - Leave all settings as default and click **"Deploy"**.
   - Vercel will automatically detect `vercel.json` and deploy your Python API.

3. **Usage:**
   - Once deployed, Vercel will give you a domain (e.g., `https://ytomnix-api.vercel.app`).
   - Add `/omnixyt/live/<VIDEO_ID>` to the end of it to play a stream!

## Local Testing
If you have Python installed, you can run it locally:
```bash
pip install -r requirements.txt
python app.py
```
Then visit `http://localhost:5000/omnixyt/live/dQw4w9WgXcQ` in your browser.
