import os

# Base directory for the camera stream service
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Log file path for the stream service
LOG_FILE = os.path.join(BASE_DIR, 'camera_service.log')

# Placeholder for future output directory, not used yet but good to define
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_frames')
os.makedirs(OUTPUT_DIR, exist_ok=True) # Ensure the directory exists

# Placeholder for future snippet capture interval
SNIPPET_CAPTURE_INTERVAL = 7