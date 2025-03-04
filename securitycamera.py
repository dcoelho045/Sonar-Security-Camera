import subprocess
import time

def run_script(script_name):
    return subprocess.Popen(["python3", script_name])


if __name__ == "__main__":
    try:
        print("Starting app.py...")
        app_process = run_script("CameraServer/app.py")
        time.sleep(2)

        print("Starting sonarsensor.py...")
        sensor_process = run_script("sonarsensor.py")

        app_process.wait()
        sensor_process.wait()

    except KeyboardInterrupt:
        print("Stopping both scripts...")
        app_process.terminate()
        sensor_process.terminate()
    
    finally:
        print("Cleaning up processes...")
        app_process.wait()
        sensor_process.wait()
