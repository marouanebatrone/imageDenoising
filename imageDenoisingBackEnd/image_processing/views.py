import logging
import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image as PILImage
import numpy as np
import cv2
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Image
from .serializers import ImageSerializer

logger = logging.getLogger(__name__)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {
            **serializer.data,
            'original_image': serializer.instance.original_image.url  # Include the original image URL in the response
        }
        return Response(response_data)

    @action(detail=True, methods=['post'])
    def add_noise(self, request, pk=None):
        image = self.get_object()
        noise_type = request.data.get('selected_noise')

        try:
            # Load the original image using OpenCV
            img_path = image.original_image.path
            logger.debug(f"Loading image from path: {img_path}")
            original_img = cv2.imread(img_path)
            if original_img is None:
                logger.error(f"Failed to load image from path: {img_path}")
                return Response({'status': 'error', 'message': 'Failed to load image.'}, status=400)

            # Convert BGR to RGB
            original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

            # Generate noisy image based on the noise type
            if (noise_type == 'Sel&&poivre'):
                noisy_img = self.add_salt_and_pepper_noise(original_img)
            elif (noise_type == 'Sel'):
                noisy_img = self.add_salt_noise(original_img)
            elif (noise_type == 'Poivre'):
                noisy_img = self.add_pepper_noise(original_img)
            else:
                logger.error(f"Unknown noise type: {noise_type}")
                return Response({'status': 'error', 'message': 'Unknown noise type.'}, status=400)

            # Convert the noisy image to PIL format and save to a temporary file
            temp_image = PILImage.fromarray(np.uint8(noisy_img))
            temp_file = BytesIO()
            temp_image.save(temp_file, format='JPEG')
            temp_file.seek(0)

            # Save the noisy image to the noisy_image_generated field
            noisy_image_name = f"noisy_{os.path.basename(img_path)}"
            logger.debug(f"Saving noisy image as: {noisy_image_name}")
            image.noisy_image_generated.save(noisy_image_name, ContentFile(temp_file.read()), save=True)
            
            # Verify the image has been saved
            if not image.noisy_image_generated:
                logger.error(f"Noisy image was not saved properly: {noisy_image_name}")
                return Response({'status': 'error', 'message': 'Noisy image was not saved properly.'}, status=500)
            
            image.selected_noise = noise_type
            image.save()
            logger.debug(f"Noisy image saved successfully: {image.noisy_image_generated.url}")
            return Response({'status': 'noise added', 'noise': noise_type, 'noisy_image_generated': image.noisy_image_generated.url})
        except Exception as e:
            logger.error(f"Error adding noise: {e}")
            return Response({'status': 'error', 'message': 'Error adding noise.'}, status=500)

    def add_salt_and_pepper_noise(self, image):
        row, col, _ = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i, int(num_salt)) for i in image.shape[:2]]
        out[coords[0], coords[1], :] = 255

        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i, int(num_pepper)) for i in image.shape[:2]]
        out[coords[0], coords[1], :] = 0
        
        return out
    
    def add_salt_noise(self, image):
        row, col, _ = image.shape
        amount = 0.004
        out = np.copy(image)
        
        # Salt mode
        num_salt = np.ceil(amount * image.size)
        coords = [np.random.randint(0, i, int(num_salt)) for i in image.shape[:2]]
        out[coords[0], coords[1], :] = 255
        
        return out
    
    def add_pepper_noise(self, image):
        row, col, _ = image.shape
        amount = 0.004
        out = np.copy(image)
        
        # Pepper mode
        num_pepper = np.ceil(amount * image.size)
        coords = [np.random.randint(0, i, int(num_pepper)) for i in image.shape[:2]]
        out[coords[0], coords[1], :] = 0
        
        return out
