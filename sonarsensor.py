import RPi.GPIO as GPIO
import time
import subprocess
import os
from pathlib import Path
import multiprocessing

from facecapture import FaceCapture  

# Define GPIO pins
trigPin = 4  # GP4
echoPin = 17  # GP17

# Initialize variables
duration = 0
cm = 0
inches = 0

# 250 ms * 12 = 3000 = 3 seconds
i = 0
size = 12
distance_arr = [0] * size
recording = False  # Flag to track recording state
time_flag = False # Flag to track if recording time began and movement ended

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

# checks to see if distances are below threshold 
def dist_checker(arr, size):
    for i in range(size):
        ###########################################################
        # needs to be changed > 48 to be within 4 feet of sonar
        # set to 10 for testing 
        ###########################################################
        if arr[i] > 10:
            return False
    return True
    
# removes old video files to prevent overwriting conflicts
def remove_duplicate_files(file_name):
	raw = Path(f'{file_name}.264')
	mp4 = Path(f'{file_name}.mp4')
	if raw.exists():
		os.remove(raw)
	if mp4.exists():
		os.remove(os)	
          
# calls capture_frame_with_face() - used for multiprocessing of face capture
def capture_face(video_path, face_pic_path):
    print('Beginning face capture')
    pic = FaceCapture(video_path, Path(f"CapturedFaces/{face_pic_path}.jpg"))
    result = pic.capture_frame_with_face(40)
    print('Face capture complete')

try:
    while True:
        # Ensure a clean HIGH pulse
        GPIO.output(trigPin, GPIO.LOW)
        time.sleep(0.000005)  # 5 microseconds
        GPIO.output(trigPin, GPIO.HIGH)
        time.sleep(0.00001)  # 10 microseconds
        GPIO.output(trigPin, GPIO.LOW)

        # Read the signal from the sensor
        while GPIO.input(echoPin) == 0:
            pulse_start = time.time()

        while GPIO.input(echoPin) == 1:
            pulse_end = time.time()

        # Calculate duration
        pulse_duration = pulse_end - pulse_start

        # Convert the time into a distance
        cm = (pulse_duration * 34300) / 2  # Speed of sound is 34300 cm/s
        inches = cm / 2.54

        print(f"{inches:.2f} in")

        # Store distance in array
        if i == size:
            i = 0
        distance_arr[i] = inches
        i += 1

        # Check distance array
        dist_flag = dist_checker(distance_arr, size)
        
        if dist_flag and not recording:
            print("#########################")
            print("Motion Detected Start Recording!")
            print("#########################")

            remove_duplicate_files('test_program_video')
            timestr = time.strftime("%Y-%m-%d---%H-%M-%S")

            script_dir = Path(__file__).parent

            # Define the correct paths
            video_dir = script_dir / "SecurityVideos"
            video_dir.mkdir(exist_ok=True) 
            timestr = time.strftime("%Y-%m-%d---%H-%M-%S")
            video_path = video_dir / f"security_vid{timestr}.264"
            mp4_path = video_dir / f"security_vid{timestr}.mp4"
            timestamp_pts = video_dir / f'timestamp.pts'
            
            print(f'video dir: {str(video_dir)}')
            print(f'timestr: {str(timestr)}')
            print(f'videopath: {str(video_path)}')
            print(f'mp4path: str{str(mp4_path)}')

            recording_process = subprocess.Popen([
                "rpicam-vid", "--level", "4.2", "--framerate", "60",
                "--width", "1280", "--height", "720", "--save-pts", str(timestamp_pts),
                "-o", str(video_path), "-t", "0", "--denoise", "cdn_off", "-n"
            ])  # -t 0 makes it record indefinitely

            recording = True  

        elif dist_flag is False and recording:
            if time_flag is False:
                last_motion_time = time.time()
                time_flag = True
                 
            if time.time() - last_motion_time > 10:
                print("No motion detected. Stopping recording...")
                
                recording_process.terminate()
                print('recording process terminated')
                recording_process.wait()

                subprocess.run(["ffmpeg", "-framerate", "60", "-i", str(video_path), "-c", "copy", str(mp4_path)])
                print("Recording complete.")

                face_pic_path = mp4_path.stem
                face_capture_process = multiprocessing.Process(target=capture_face, args=(video_path, face_pic_path))
                face_capture_process.start()

                recording = False 
                time_flag = False

        # Delay for 250 ms
        # 250 ms * 12 = 3000 = 3 seconds
        time.sleep(0.250)

except KeyboardInterrupt:
    GPIO.cleanup()
