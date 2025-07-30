from django.contrib import admin
from .models import Camera, FireDetection
from django.utils.safestring import mark_safe

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['name', 'camera_id', 'location', 'rtsp_url']
    list_filter = ['location']
    search_fields = ['name', 'camera_id']

@admin.register(FireDetection)
class FireDetectionAdmin(admin.ModelAdmin):
    list_display = ['camera_id', 'severity_level', 'confidence', 'timestamp', 'is_resolved','image_preview']
    list_filter = ['is_resolved', 'camera_id', 'timestamp']
    search_fields = ['camera_id', 'farm_id', 'notes']
    readonly_fields = ['timestamp', 'confidence', 'camera_id', 'farm_id']
    
    def severity_level(self, obj):
        return obj.severity_level
    severity_level.short_description = 'Severity'
    def image_preview(self, obj):
        if obj.image_data:
            return mark_safe(f'<img src="data:image/jpeg;base64,{obj.image_data}" style="max-width: 200px; max-height: 200px;">')
        return "No image"
    image_preview.short_description = "Image Preview"

# Register your models here.
