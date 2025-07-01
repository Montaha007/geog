from django.db import models
from geo.models import Location

from django.db import models
from geo.models import Location

class Camera(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)  # <-- allow blank
    stream_id = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='cameras')

    def save(self, *args, **kwargs):
        # Auto-generate name if it's not provided
        if not self.name:
            self.name = f"Camera at {self.location.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or self.stream_id

