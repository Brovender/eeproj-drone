import cv2                     # OpenCV - used here for JPEG compression
import imagezmq               # Library for sending images over network (ZeroMQ)
from picamera2 import Picamera2  # Raspberry Pi camera interface
from picamera2.outputs import FileOutput  # (Not used here, can be removed)
import io                     # (Not used here, can be removed)

# --- CONFIG ---
SERVER_IP = "10.111.252.26"   # IP address of the receiving PC/server
SERVER_PORT = "5555"          # Port used for sending images
JPEG_QUALITY = 40             # JPEG compression quality (1-100)
                              # Lower = faster + less bandwidth, Higher = better quality
# --------------

def run_streamer():
    # Create a sender object that connects to the server via TCP
    # This is what sends the images over the network
    sender = imagezmq.ImageSender(connect_to=f"tcp://{SERVER_IP}:{SERVER_PORT}")

    # Initialize the Raspberry Pi camera
    picam2 = Picamera2()

    # Configure the camera:
    # - Resolution: 640x480 (keeps things fast)
    # - Format: RGB888 (3 channels → avoids 4-channel errors)
    config = picam2.create_video_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )

    picam2.configure(config)  # Apply configuration
    picam2.start()            # Start the camera

    print(f"Streaming compressed MJPEG to {SERVER_IP}...")

    try:
        # Main loop: capture → compress → send
        while True:
            # Capture a single frame as a NumPy array
            frame = picam2.capture_array()

            # Compress the frame into JPEG format (in memory)
            # This drastically reduces size compared to raw image
            ret, buffer = cv2.imencode(
                '.jpg',                      # Encode as JPEG
                frame,                       # Input image
                [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]  # Compression level
            )

            # If encoding was successful, send the image
            if ret:
                # "pi_cam" is just a name/id for this camera stream
                sender.send_jpg("pi_cam", buffer)

    except KeyboardInterrupt:
        # Allows clean exit when pressing Ctrl+C
        pass

    finally:
        # Always stop the camera when exiting
        picam2.stop()


# Run the streamer only if this file is executed directly
if __name__ == "__main__":
    run_streamer()
