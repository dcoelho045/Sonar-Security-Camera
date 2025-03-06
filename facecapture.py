import cv2
print(f'cv2: {str(cv2.__version__)}')
import os

class FaceCapture():
    def __init__(self, video_path, output_image_path):
        self.video_path = video_path
        self.output_image_path = output_image_path


    def capture_frame_with_face(self, max_frames, cascade_path="haarcascade_frontalface_default.xml"):
        flag = False
        # Load the face detection model
        face_cascade = cv2.CascadeClassifier(cascade_path)
        video_capture = cv2.VideoCapture(str(self.video_path))
        
        if not video_capture.isOpened():
            raise Exception(f"Failed to open video: {self.video_path}")
        print('opened video')

        frames_with_faces = []
        
        while True:
            # Read the next frame
            ret, frame = video_capture.read()
            print(f'ret: {str(ret)}\nframe: {str(frame)}')
            if not ret:
                print("No more frames to read.")
                flag = False
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
            cv2.imwrite(str(self.output_image_path), frames_with_faces[len(frames_with_faces) - 1])
            print(f"Face detected. Frame saved to {self.output_image_path}")
            flag = True
        
        video_capture.release()
        return flag

if __name__ == "__main__":
    video_directory = "SecurityVideos"
    output_directory = "CapturedFaces"
    os.makedirs(output_directory, exist_ok=True)

    video_path = os.path.join(video_directory, 'security_vid2025-03-05---19-49-47.mp4')
    output_image_path = os.path.join(output_directory, f"security_vid2025-03-05---19-49-47.jpg")

    pic = FaceCapture(video_path, output_image_path)
    pic_result = pic.capture_frame_with_face(40)
