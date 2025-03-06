import os
import pathlib
from flask import Flask, render_template, send_from_directory, abort

app = Flask(__name__)

BASE_DIR = pathlib.Path(__file__).parent.parent
VIDEO_DIR = BASE_DIR / "SecurityVideos"
IMAGE_DIR = BASE_DIR / "CapturedFaces"

@app.route("/")
def index():
    # List all .mp4 files in the SecurityVideos directory
    videos = sorted(
        [f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")],
        key=lambda f: os.path.getctime(os.path.join(VIDEO_DIR, f)),  # Sort by creation time
        reverse=True  # Newest first
    )

    # Check if there is a corresponding image for each video
    video_data = []
    for video in videos:
        video_name = os.path.splitext(video)[0]  # Remove .mp4 extension
        image_path = IMAGE_DIR / f"{video_name}.jpg"
        has_image = image_path.exists()
        video_data.append({
            "filename": video,
            "has_image": has_image,
            "image_filename": f"{video_name}.jpg" if has_image else None
        })

    return render_template("index.html", videos=video_data)

# Route to serve video files from the SecurityVideos directory
@app.route("/videos/<filename>")
def serve_video(filename):
    file_path = VIDEO_DIR / filename
    if not file_path.exists():
        abort(404, description="Video not found")
    return send_from_directory(VIDEO_DIR, filename)

# Route to serve image files from the CapturedFaces directory
@app.route("/images/<filename>")
def serve_image(filename):
    file_path = IMAGE_DIR / filename
    if not file_path.exists():
        abort(404, description="Image not found")
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# website link: http://192.168.1.89:5000/
