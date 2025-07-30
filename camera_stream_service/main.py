import logging
import time
import sys
import os
import threading
import signal
from celery import Celery
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from cams.models import Camera  # Import your Camera model
from .camera_manager import CameraManager
from .fire_alert_listener import FireAlertListener
from .config import LOG_FILE

shutdown_requested = threading.Event()

def signal_handler(signum, frame):
    logger.info(f"Signal {signum} received, requesting shutdown...")
    shutdown_requested.set()

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# --- Celery Configuration ---
celery_app = Celery('stream_worker_celery_client', broker='redis://localhost:6379/0')

def run_stream_worker():
    logger.info("Starting Camera Stream Worker Service...")

    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)

    manager = CameraManager(celery_app=celery_app)

    fire_listener = FireAlertListener()
    fire_thread = threading.Thread(target=fire_listener.start_listening, daemon=True)
    fire_thread.start()
    logger.info("🔥 Fire alert listener started")

    cameras = Camera.objects.all()
    for cam in cameras:
        rtsp_url = cam.rtsp_url
        manager.start_camera_stream(cam.camera_id, rtsp_url, cam.name)

    logger.info("Camera streams started. Press Ctrl+C to stop.")

    try:
        while not shutdown_requested.is_set():
            if shutdown_requested.wait(timeout=1.0):
                break
    except KeyboardInterrupt:
        logger.info("Ctrl+C detected. Initiating graceful shutdown...")
        shutdown_requested.set()
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
        shutdown_requested.set()
    finally:
        logger.info("Starting cleanup process...")

        try:
            logger.info("Stopping fire alert listener...")
            fire_listener.stop_listening()
            if fire_thread.is_alive():
                logger.info("Waiting for fire alert listener to stop...")
                fire_thread.join(timeout=3.0)
                if fire_thread.is_alive():
                    logger.warning("Fire alert listener thread did not stop gracefully")
        except Exception as e:
            logger.error(f"Error stopping fire alert listener: {e}")

        try:
            logger.info("Stopping all camera streams...")
            manager.shutdown_all_streams()
        except KeyboardInterrupt:
            logger.warning("Camera shutdown interrupted, forcing immediate exit...")
        except Exception as e:
            logger.error(f"Error during camera shutdown: {e}")

        logger.info("Camera Stream Worker Service stopped.")

if __name__ == '__main__':
    run_stream_worker()
