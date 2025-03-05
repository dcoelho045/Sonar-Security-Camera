import cv2
import os

def capture_frame_from_video(video_path, output_image_path):
    # Load the video
    video_capture = cv2.VideoCapture(video_path)
    
    if not video_capture.isOpened():
        raise Exception(f"Failed to open video: {video_path}")

    # Read the first frame
    ret, frame = video_capture.read()

    if ret:
        # Save the entire frame as a JPEG file
        cv2.imwrite(output_image_path, frame)
        print(f"Frame saved to {output_image_path}")
    else:
        print("Failed to capture a frame from the video.")

    # Release the video capture object
    video_capture.release()

# Example usage
video_directory = "SecurityVideos"
output_directory = "CapturedFaces"  

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Process each video in the directory
video_path = os.path.join(video_directory, 'security_vid2025-03-04---13-27-26.mp4')
output_image_path = os.path.join(output_directory, f"security_vid2025-03-04---13-27-26.jpg")
capture_frame_from_video(video_path, output_image_path)

# security_vid2025-03-04---13-27-26.mp4
# security_vid2025-03-04---23-41-21.mp4