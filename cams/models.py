from django.db import models
from geo.models import Location
import os
from django.conf import settings
import subprocess  # Add this import at the top
from django.utils import timezone

class Camera(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    camera_id = models.CharField(max_length=100, unique=True, help_text="Used in go2rtc config (e.g., cam1)" ,default="")
    rtsp_url = models.CharField(max_length=500, help_text="RTSP URL for FFmpeg processing or go2rtc.", default="")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='cameras')

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"Camera at {self.location.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or self.camera_id


    def get_stream_url(self):
        return f"http://localhost:1984/stream.html?src={self.camera_id}"

    def get_go2rtc_url(self):
        return f"http://localhost:1984/api/streams/{self.camera_id}"

    def get_go2rtc_iframe_url(self):
        return f"http://localhost:1984/streams/{self.camera_id}"

    def get_hls_url(self):
        return f"http://localhost:1984/api/streams/{self.camera_id}.m3u8"

    def stream_file_to_rtsp(self, input_file, loop=True):
        """
        Stream a local video file to this camera's go2rtc RTSP endpoint.
        """
        rtsp_target = f"rtsp://localhost:8554/{self.camera_id}"
        cmd = [
            'ffmpeg',
            '-re',
        ]
        if loop:
            cmd += ['-stream_loop', '-1']
        cmd += [
            '-i', input_file,
            '-c', 'copy',
            '-f', 'rtsp',
            rtsp_target
        ]
        # Start FFmpeg as a background process
        subprocess.Popen(cmd)
        return rtsp_target

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

class FireDetection(models.Model):
    """Store fire detection results"""
    camera_id = models.CharField(max_length=100, help_text="Camera stream ID")
    farm_id = models.CharField(max_length=100, help_text="Farm/Location ID") 
    confidence = models.FloatField(help_text="Detection confidence (0.0 to 1.0)")
    timestamp = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False, help_text="Has this alert been handled?")
    notes = models.TextField(blank=True, help_text="Additional notes about this detection")
    image_data = models.TextField(null=True, blank=True)  # Store base64 image data
    bounding_box = models.JSONField(null=True, blank=True)
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Fire Detection"
        verbose_name_plural = "Fire Detections"
        
    def __str__(self):
        return f"Fire detected - {self.camera_id} at {self.timestamp} (confidence: {self.confidence:.2f})"
        
    @property
    def image_url(self):
        """Return data URL for direct display in frontend"""
        if self.image_data:
            return f"data:image/jpeg;base64,{self.image_data}"
        return None
    @property
    def severity_level(self):
        """Return severity based on confidence"""
        if self.confidence >= 0.9:
            return "CRITICAL"
        elif self.confidence >= 0.7:
            return "HIGH"
        elif self.confidence >= 0.5:
            return "MEDIUM"
        else:
            return "LOW"