import cv2
import imagezmq
from picamera2 import Picamera2
from picamera2.outputs import FileOutput
import io

# --- CONFIG ---
SERVER_IP = "10.111.252.26"
SERVER_PORT = "5555"
JPEG_QUALITY = 40  # Lower = faster/lower bandwidth (1-100)
# --------------

def run_streamer():
    sender = imagezmq.ImageSender(connect_to=f"tcp://{SERVER_IP}:{SERVER_PORT}")
    picam2 = Picamera2()
    # Request BGR888 directly to avoid the 4-channel error
    config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()

    print(f"Streaming compressed MJPEG to {SERVER_IP}...")
    
    try:
        while True:
            frame = picam2.capture_array()
            
            # Compress to JPEG in memory
            # This is much smaller than sending a raw numpy array
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
            
            if ret:
                sender.send_jpg("pi_cam", buffer)
    except KeyboardInterrupt:
        pass
    finally:
        picam2.stop()

if __name__ == "__main__":
    run_streamer()
