from concurrent.futures import thread
import logging 
import time
from typing import Any, Dict, List, Optional
import threading
from celery import Celery

from .camera_thread import CameraThread

logger = logging.getLogger(__name__)

class CameraManager:
    """ manages multiple camera threads     
    """
    def __init__(self, celery_app: Celery):
        """Initializes the CameraManager."""
        #Dictionary to hold camera threads
        self.active_camera_threads: Dict[str, CameraThread] = {}
        self.celery_app = celery_app # Store the Celery app instance for later use
        logger.info("CameraManager initialized.")
        
    def start_camera_stream(self, camera_id: str, rtsp_url: str, name: str) -> bool:
        """Starts a camera stream by creating and starting a CameraThread.

        Args:
            camera_id (str): Unique identifier for the camera.
            rtsp_url (str): RTSP URL of the camera stream.
            name (str): Display name of the camera.

        Returns:
            bool: True if the thread was started successfully, False if it already exists.
        """
        if camera_id in self.active_camera_threads:
            logger.warning(f"Camera thread for ID '{camera_id}' already exists. stopping and restarting it.")
            self.stop_camera_stream(camera_id)
            time.sleep(0.1)
        try:
            # Create a Celery task signature for the fire detection task
            ai_detection_task_signature = self.celery_app.signature('fire_detection_service.fire_detector.detect_fire_task')

            thread = CameraThread(camera_id, rtsp_url, name, ai_detection_task_signature)
            thread.start()
            self.active_camera_threads[camera_id] = thread
            logger.info(f"Camera thread for '{name}' (ID: {camera_id}) started successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to start camera thread for '{name}' (ID: {camera_id}): {e}", exc_info=True)
            # If an error occurs, we log it and return False
            return False
            
    def stop_camera_stream(self, camera_id: str) -> bool:
        """
        Signals a camera stream thread to stop gracefully.
        Args:
            camera_id (str): The ID of the camera stream to stop.
        Returns:
            bool: True if the stream was found and stopped, False otherwise.
        """
        if camera_id in self.active_camera_threads:
            thread = self.active_camera_threads[camera_id]
            logger.info(f"Stopping camera thread for ID '{camera_id}'...")
            thread.stop() # Signal the thread to stop
            
            # Wait for the thread to terminate with timeout, but handle interrupts
            try:
                thread.join(timeout=3) # Reduced timeout to 3 seconds
                
                if thread.is_alive():
                    logger.warning(f"Camera thread for ID '{camera_id}' did not terminate gracefully within timeout.")
                    # Force cleanup if thread is still alive
                    try:
                        if hasattr(thread, 'cap') and thread.cap:
                            thread.cap.release()
                            logger.info(f"Force released video capture for camera '{camera_id}'")
                    except Exception as e:
                        logger.error(f"Error in force cleanup for camera '{camera_id}': {e}")
                else:
                    logger.info(f"Camera thread for ID '{camera_id}' stopped successfully.")
                    
            except KeyboardInterrupt:
                logger.warning(f"Shutdown interrupted for camera '{camera_id}', forcing cleanup...")
                # Force cleanup on interrupt
                try:
                    if hasattr(thread, 'cap') and thread.cap:
                        thread.cap.release()
                        logger.info(f"Force released video capture for camera '{camera_id}' after interrupt")
                except Exception as e:
                    logger.error(f"Error in force cleanup after interrupt for camera '{camera_id}': {e}")
            
            del self.active_camera_threads[camera_id] # Remove from active threads dictionary
            return True
        else:
            logger.warning(f"Attempted to stop non-existent stream for camera ID '{camera_id}'.")
            return False
            
    def get_camera_status(self, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Gets the current status of a specific camera stream.
        Args:
            camera_id (str): The ID of the camera.
        Returns:
            Optional[Dict]: A dictionary with status information, or None if the camera is not found.
        """
        thread = self.active_camera_threads.get(camera_id)
        if thread:
            return thread.get_status() # Delegate to the CameraThread's get_status method
        return None
        
    def get_all_camera_statuses(self) -> Dict[str, Dict[str, Any]]:
        """
        Gets the status of all active camera streams.
        Returns:
            Dict[str, Dict]: A dictionary of statuses, keyed by camera_id.
        """
        statuses = {}
        # Iterate over a copy of keys to safely modify the dictionary if threads die
        for camera_id in list(self.active_camera_threads.keys()):
            thread = self.active_camera_threads[camera_id]
            if thread.is_alive():
                statuses[camera_id] = thread.get_status()
            else:
                logger.warning(f"Detected dead thread for camera ID '{camera_id}'. Removing from manager.")
                del self.active_camera_threads[camera_id] # Clean up dead threads
        return statuses

    def shutdown_all_streams(self):
        """
        Gracefully stops all active camera streams managed by this CameraManager.
        """
        logger.info("Shutting down all active camera streams...")
        # Iterate over a copy of keys as stop_camera_stream modifies the dictionary
        camera_ids = list(self.active_camera_threads.keys())
        
        try:
            for camera_id in camera_ids:
                try:
                    self.stop_camera_stream(camera_id)
                except KeyboardInterrupt:
                    logger.warning(f"Shutdown interrupted while stopping camera '{camera_id}', continuing with force cleanup...")
                    # Force cleanup remaining cameras
                    for remaining_id in camera_ids:
                        if remaining_id in self.active_camera_threads:
                            thread = self.active_camera_threads[remaining_id]
                            try:
                                if hasattr(thread, 'cap') and thread.cap:
                                    thread.cap.release()
                                    logger.info(f"Force released video capture for camera '{remaining_id}'")
                            except Exception as e:
                                logger.error(f"Error in force cleanup for camera '{remaining_id}': {e}")
                            del self.active_camera_threads[remaining_id]
                    break
                except Exception as e:
                    logger.error(f"Error stopping camera '{camera_id}': {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in shutdown_all_streams: {e}")
        finally:
            # Clear any remaining threads
            self.active_camera_threads.clear()
            logger.info("All camera streams shut down.")
