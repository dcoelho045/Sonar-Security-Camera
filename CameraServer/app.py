import os
import pathlib
import flask
from flask import Flask, render_template, send_from_directory, abort


app = Flask(__name__)

# Get the absolute path of the parent directory (where SecurityVideos is located)
BASE_DIR = pathlib.Path(__file__).parent.parent

# Path to the SecurityVideos directory
VIDEO_DIR = BASE_DIR / "SecurityVideos"

@app.route("/")
def index():
    # List all .mp4 files in the SecurityVideos directory
    # videos = [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")]
    # return render_template("index.html", videos=videos)
	videos = sorted(
		[f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")],
		key=lambda f: os.path.getctime(os.path.join(VIDEO_DIR, f)),  # Sort by creation time
		reverse=True  # Newest first
	)
	return render_template("index.html", videos=videos)

# Route to serve video files from the SecurityVideos directory
@app.route("/videos/<filename>")
def serve_video(filename):
    file_path = VIDEO_DIR / filename
    if not file_path.exists():  # Check if file exists
        abort(404, description="Video not found")
    return send_from_directory(VIDEO_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# http://192.168.1.89:5000/
