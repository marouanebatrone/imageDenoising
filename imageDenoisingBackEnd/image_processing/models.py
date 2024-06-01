from django.db import models
from django.utils import timezone

class Image(models.Model):
    original_image = models.ImageField(upload_to='images/')
    selected_noise = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)
    noisy_image_generated = models.ImageField(upload_to='noisy_images/', null=True, blank=True)
    filtered_image = models.ImageField(upload_to='filtered_images/', null=True, blank=True)
