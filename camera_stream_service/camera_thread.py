import os
import threading
import time
import logging
import cv2
import base64
from typing import Callable, Any

# Import LOG_FILE from our config.py
from .config import LOG_FILE, OUTPUT_DIR, SNIPPET_CAPTURE_INTERVAL

# Set up logging for this module
# We'll configure the handlers (e.g., FileHandler, StreamHandler) in main.py
# For now, just get the logger instance.
logger = logging.getLogger(__name__)

class CameraThread(threading.Thread):
    """
    A basic thread structure for handling a single camera stream.
    It includes mechanisms for graceful stopping and simulates work.
    """
    def __init__(self, camera_id: str, rtsp_url: str, name: str, ai_task: Callable[..., Any]):
        """
        Initializes the CameraThread.
        Args:
            stream_id (str): Unique ID of the camera.
            rtsp_url (str): RTSP URL of the camera stream (placeholder for now).
            name (str): Display name of the camera.
        """
        super().__init__()
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.name = name
        self.cap = None # OpenCV VideoCapture object
        self._stop_event = threading.Event() # Event to signal the thread to stop
        self.is_running = False # Flag to indicate if the thread's main loop is active
        self.ai_task= ai_task
        self.last_snippet_time = time.time()

        logger.info(f"CameraThread for '{self.name}' (ID: {self.camera_id}) initialized.")
    
    def run(self):
        """
        Main method of the thread. Continuously reads the RTSP feed.
        """
        logger.info(f"Starting stream for camera '{self.name}' (ID: {self.camera_id})...")
        self.is_running = True
        
        while not self._stop_event.is_set():
            try:
                # Attempt to open/reopen the video capture if not already open
                if self.cap is None or not self.cap.isOpened():
                    logger.info(f"Attempting to open RTSP stream for '{self.name}' at {self.rtsp_url}")
                    # Use CAP_FFMPEG for better compatibility with various RTSP streams
                    self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
                    
                    # Set buffer size to reduce latency and make frame reading more responsive
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    
                    if not self.cap.isOpened():
                        logger.error(f"Failed to open RTSP stream for '{self.name}'. Retrying in 5 seconds...")
                        # Use interruptible sleep
                        if self._stop_event.wait(timeout=5.0):
                            break
                        continue # Skip to the next iteration of the loop

                # Check stop event before attempting to read frame
                if self._stop_event.is_set():
                    break

                ret, frame = self.cap.read() # Read a frame from the stream
                if not ret:
                    logger.warning(f"Failed to read frame from '{self.name}'. Releasing and re-opening stream...")
                    self.cap.release() # Release the capture object
                    self.cap = None # Set to None to force re-opening on next loop iteration
                    # Use interruptible sleep
                    if self._stop_event.wait(timeout=1.0):
                        break
                    continue # Skip to the next iteration of the loop

                # Check stop event before processing frame
                if self._stop_event.is_set():
                    break

                # Process the frame (e.g., save snippet)
                self._process_frame(frame)

                # Use interruptible sleep to prevent busy-waiting and reduce CPU usage
                if self._stop_event.wait(timeout=0.01):
                    break

            except Exception as e:
                logger.error(f"Error in CameraThread for '{self.name}': {e}", exc_info=True)
                # Ensure capture object is released on error
                if self.cap:
                    self.cap.release()
                self.cap = None # Reset to force re-opening
                # Use interruptible sleep
                if self._stop_event.wait(timeout=5.0):
                    break

        logger.info(f"Stopping stream for camera '{self.name}' (ID: {self.camera_id}).")
        if self.cap:
            self.cap.release() # Release resources when stopping
        self.is_running = False


    def _process_frame(self, frame):
        """
        Internal method to process a single frame.
        Captures snippets periodically. Ensures parallel output by writing to per-thread directory.
        """
        current_time = time.time()
        if current_time - self.last_snippet_time >= SNIPPET_CAPTURE_INTERVAL:
            # Create a per-stream output directory for parallelism
            stream_output_dir = os.path.join(OUTPUT_DIR, self.camera_id)
            os.makedirs(stream_output_dir, exist_ok=True)
            snippet_filename = os.path.join(stream_output_dir, f"{int(current_time)}.jpg")
            try:
                # Save the frame as a JPEG snippet
                result = cv2.imwrite(snippet_filename, frame)
                if result:
                    logger.info(f"[PARALLEL] Captured snippet for '{self.name}' in {stream_output_dir}: {snippet_filename}")
                else:
                    logger.error(f"cv2.imwrite failed for '{self.name}' at {snippet_filename}")
                    return  # Skip fire detection if frame save failed
                    
                self.last_snippet_time = current_time
                
                # Push to Celery/AI service asynchronously
                # Convert frame to base64 for fire detection task
                _, buffer = cv2.imencode('.jpg', frame)
                frame_b64 = base64.b64encode(buffer).decode('utf-8')
                
                # Send frame for fire detection with correct parameters
                detection_result = self.ai_task.delay(
                    frame_b64=frame_b64,
                    camera_id=self.camera_id,
                    name=self.name
                )
                logger.info(f"Pushed frame for fire detection from camera {self.camera_id} (Task ID: {detection_result.id})")
                
            except Exception as e:
                logger.error(f"Failed to save snippet for '{self.name}': {e}")
    def stop(self):
        """
        Signals the thread to stop gracefully.
        Sets the internal stop event, which will cause the run() method's loop to exit.
        """
        logger.info(f"Stop signal received for camera '{self.name}' (ID: {self.camera_id}).")
        self._stop_event.set()
        
        # Force release video capture to unblock any pending read operations
        if self.cap and self.cap.isOpened():
            try:
                self.cap.release()
                logger.info(f"Released video capture for camera '{self.name}'")
            except Exception as e:
                logger.error(f"Error releasing video capture for '{self.name}': {e}")
            finally:
                self.cap = None

    def is_stopped(self) -> bool:
        """
        Checks if the thread has been signaled to stop.
        Returns:
            bool: True if the stop event is set, False otherwise.
        """
        return self._stop_event.is_set()

    def get_status(self) -> dict:
        """
        Returns a dictionary containing the current status of the camera thread.
        """
        return {
            "camera_id": self.camera_id,
            "name": self.name,
            "rtsp_url": self.rtsp_url,
            "is_running": self.is_running,
            "is_alive": self.is_alive(), # threading.Thread method to check if thread is active
            "stop_signaled": self.is_stopped()
        }