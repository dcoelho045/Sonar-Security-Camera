import cv2
print(f'cv2: {str(cv2.__version__)}')
import os

def capture_frame_with_face(video_path, output_image_path, max_frames, cascade_path="haarcascade_frontalface_default.xml"):
    # Load the face detection model
    face_cascade = cv2.CascadeClassifier(cascade_path)
    video_capture = cv2.VideoCapture(video_path)
    
    if not video_capture.isOpened():
        raise Exception(f"Failed to open video: {video_path}")
    print('opened video')

    frames_with_faces = []
    
    while True:
        # Read the next frame
        ret, frame = video_capture.read()
        print(f'ret: {str(ret)}\nframe: {str(frame)}')
        if not ret:
            print("No more frames to read.")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        if len(faces) > 0:
            # If a face is detected, save the frame to the array
            frames_with_faces.append(frame)
            print(f"Face detected in frame. Total frames with faces: {len(frames_with_faces)}")
            
            # Stop if we have collected the desired number of frames
            if len(frames_with_faces) >= max_frames:
                break
    
    print(len(frames_with_faces))
    if len(frames_with_faces) > 0:
        cv2.imwrite(output_image_path, frames_with_faces[len(frames_with_faces) - 1])
        print(f"Face detected. Frame saved to {output_image_path}")
    
    video_capture.release()

# Example usage
video_directory = "SecurityVideos"
output_directory = "CapturedFaces"
os.makedirs(output_directory, exist_ok=True)

video_path = os.path.join(video_directory, 'security_vid2025-03-04---13-27-26.mp4')
output_image_path = os.path.join(output_directory, f"security_vid2025-03-04---13-27-26.jpg")

capture_frame_with_face(video_path, output_image_path, 40)
