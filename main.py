from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "KBG VIP SERVER IS LIVE"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            real_url = info.get('url')
            if not real_url and 'entries' in info:
                real_url = info['entries'][0]['url']

            if not real_url:
                return jsonify({"status": "error", "message": "Could not find video link"}), 404

            return jsonify({
                "status": "success",
                "url": real_url
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Ab 5000 port use hogi jo Replit par error nahi degi
    app.run(host='0.0.0.0', port=5000)