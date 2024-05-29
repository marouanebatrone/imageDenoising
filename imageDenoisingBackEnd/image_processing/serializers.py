from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'original_image', 'selected_noise', 'timestamp', 'noisy_image_generated']

