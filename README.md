# Pi Streamer (Camera Module 3)

Captures high-speed video using `Picamera2` and streams compressed MJPEG frames to the central server via `ImageZMQ`.

## Setup & Execution

1. **Hardware Check:**
   - Ensure the Camera Module 3 is connected
   - Run `libcamera-hello` to verify the camera is detected

2. **Install Dependencies:**
   ```bash
   # Note: Use --system-site-packages if creating a venv to access libcamera
   pip install --system-site-packages -r requirements.txt 
   ```

3. **Configure Connection:**
   - Open `pi_streamer.py`
   - Update `SERVER_IP` to match your Server's IP address
   - Ensure `SERVER_PORT` is `5555` (or whatever you set it in the server software)

4. **Run the Streamer:**
   ```bash
   chmod +x start_pi.sh
   ./start_pi.sh
   ```

##Performance Tuning
- **Latency:** Decrease `JPEG_QUALITY` (e.g., to 30) for faster transmission on slow WiFi.
- **Framerate:** If the server is "sticking," add a small `time.sleep(0.03)` in the capture loop to throttle output.
