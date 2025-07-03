from django.db import models
from geo.models import Location
import os
from django.conf import settings
import subprocess  # Add this import at the top

class Camera(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    stream_id = models.CharField(max_length=100, unique=True, help_text="Used in go2rtc config (e.g., cam1)" ,default="")
    rtsp_url = models.CharField(max_length=500, help_text="RTSP URL for FFmpeg processing or go2rtc.", default="")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='cameras')

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"Camera at {self.location.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or self.stream_id


    def get_stream_url(self):
        return f"http://localhost:1984/stream.html?src={self.stream_id}"

    # ✅ Stream URL (go2rtc live streaming)
    def get_go2rtc_url(self):
        return f"http://localhost:1984/api/streams/{self.stream_id}"

    # ✅ Web player iframe embed (if using go2rtc's built-in player)
    def get_go2rtc_iframe_url(self):
        return f"http://localhost:1984/streams/{self.stream_id}"

    # ✅ HLS URL (for <video> tag + hls.js)
    def get_hls_url(self):
        return f"http://localhost:1984/api/streams/{self.stream_id}.m3u8"

    # ✅ Optional FFmpeg recording


    def record_clip(self, duration=10):
        """
        Start FFmpeg to record a short clip from the camera.
        """
        output_dir = os.path.join(settings.MEDIA_ROOT, 'recordings', f'camera_{self.id}')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'clip.mp4')
        error_log = os.path.join(output_dir, 'ffmpeg_error.log')

        ffmpeg_command = [
            'ffmpeg',
            '-y',  # overwrite
            '-rtsp_transport', 'tcp',
            '-i', self.rtsp_url.strip(),
            '-t', str(duration),
            '-c:v', 'copy',
            output_path
        ]

        with open(error_log, 'w') as err:
            subprocess.run(ffmpeg_command, stderr=err, stdout=subprocess.DEVNULL)

        return output_path