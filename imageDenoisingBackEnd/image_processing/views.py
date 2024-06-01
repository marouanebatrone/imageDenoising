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
from skimage import util,io

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
            'original_image': serializer.instance.original_image.url 
        }
        return Response(response_data)

    @action(detail=True, methods=['post'])
    def add_noise(self, request, pk=None):
        image = self.get_object()
        noise_type = request.data.get('selected_noise')

        try:
            img_path = image.original_image.path
            img = PILImage.open(img_path)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                img.save(img_path)
            original_img = cv2.imread(img_path)
            if original_img is None:
                logger.error(f"Failed to load image from path: {img_path}")
                return Response({'status': 'error', 'message': 'Failed to load image.'}, status=400)

            original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

            if noise_type == 'Sel&&poivre':
                noisy_img = self.add_salt_and_pepper_noise(original_img)
            elif noise_type == 'Sel':
                noisy_img = self.add_salt_noise(original_img)
            elif noise_type == 'Poivre':
                noisy_img = self.add_pepper_noise(original_img)
            elif noise_type == 'Gaussian':
                original_img = io.imread(img_path)
                noisy_img = self.add_gaussien_noise(original_img)
            else:
                logger.error(f"Unknown noise type: {noise_type}")
                return Response({'status': 'error', 'message': 'Unknown noise type.'}, status=400)

            temp_image = PILImage.fromarray(np.uint8(noisy_img))
            temp_file = BytesIO()
            temp_image.save(temp_file, format='JPEG')
            temp_file.seek(0)

            noisy_image_name = f"noisy_{os.path.basename(img_path)}"
            image.noisy_image_generated.save(noisy_image_name, ContentFile(temp_file.read()), save=True)

            if not image.noisy_image_generated:
                logger.error(f"Noisy image was not saved properly: {noisy_image_name}")
                return Response({'status': 'error', 'message': 'Noisy image was not saved properly.'}, status=500)

            image.selected_noise = noise_type
            image.save()
            return Response({'status': 'noise added', 'noise': noise_type, 'noisy_image_generated': image.noisy_image_generated.url})
        except Exception as e:
            logger.error(f"Error adding noise: {e}")
            return Response({'status': 'error', 'message': 'Error adding noise.'}, status=500)

    @action(detail=True, methods=['post'])
    def apply_filter(self, request, pk=None):
        image = self.get_object()
        filter_type = request.data.get('selected_filter')

        try:
            img_path = image.noisy_image_generated.path
            original_img = cv2.imread(img_path)
            if original_img is None:
                logger.error(f"Failed to load image from path: {img_path}")
                return Response({'status': 'error', 'message': 'Failed to load image.'}, status=400)

            original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

            if filter_type == 'filtre_gaussien':
                filtered_img = self.apply_gaussian_filter(original_img)
            elif filter_type == 'filtre_median':
                filtered_img = self.apply_median_filter(original_img)
            elif filter_type == 'filtre_mean':
                filtered_img = self.apply_mean_filter(original_img)
            elif filter_type == 'filtre_min':
                filtered_img = self.apply_min_filter(original_img)
            elif filter_type == 'filtre_max':
                filtered_img = self.apply_max_filter(original_img)
            else:
                logger.error(f"Unknown filter type: {filter_type}")
                return Response({'status': 'error', 'message': 'Unknown filter type.'}, status=400)

            temp_image = PILImage.fromarray(np.uint8(filtered_img))
            temp_file = BytesIO()
            temp_image.save(temp_file, format='JPEG')
            temp_file.seek(0)

            filtered_image_name = f"filtered_{os.path.basename(img_path)}"
            image.filtered_image.save(filtered_image_name, ContentFile(temp_file.read()), save=True)

            if not image.filtered_image:
                logger.error(f"Filtered image was not saved properly: {filtered_image_name}")
                return Response({'status': 'error', 'message': 'Filtered image was not saved properly.'}, status=500)

            return Response({'status': 'filter applied', 'filter': filter_type, 'filtered_image_url': image.filtered_image.url})
        except Exception as e:
            logger.error(f"Error applying filter: {e}")
            return Response({'status': 'error', 'message': 'Error applying filter.'}, status=500)

    def add_salt_and_pepper_noise(self, image):
        row, col, _ = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i, int(num_salt)) for i in image.shape[:2]]
        out[coords[0], coords[1], :] = 255

        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i, int(num_pepper)) for i in image.shape[:2]]
        out[coords[0], coords[1], :] = 0
        
        return out
    
    def add_salt_noise(self, image):
        row, col, _ = image.shape
        amount = 0.004
        out = np.copy(image)
        
        num_salt = np.ceil(amount * image.size)
        coords = [np.random.randint(0, i, int(num_salt)) for i in image.shape[:2]]
        out[coords[0], coords[1], :] = 255
        
        return out
    
    def add_pepper_noise(self, image):
        row, col, _ = image.shape
        amount = 0.004
        out = np.copy(image)
        
        num_pepper = np.ceil(amount * image.size)
        coords = [np.random.randint(0, i, int(num_pepper)) for i in image.shape[:2]]
        out[coords[0], coords[1], :] = 0
        
        return out
    
    def add_gaussien_noise(self, image):
        out = np.copy(image)
        out = util.random_noise(out, mode='gaussian', mean=0, var=0.01)
        out = (out * 255).astype(np.uint8)
        return out
    
    
    # Filters methods defenitions:

    def apply_gaussian_filter(self, image):
        return cv2.GaussianBlur(image, (5, 5), 0)

    def apply_median_filter(self, image):
        return cv2.medianBlur(image, 5)

    def apply_mean_filter(self, image):
        kernel = np.ones((5, 5), np.float32) / 25
        return cv2.filter2D(image, -1, kernel)

    def apply_min_filter(self, image):
        return cv2.erode(image, np.ones((5,5),np.uint8))

    def apply_max_filter(self, image):
        return cv2.dilate(image, np.ones((5,5),np.uint8))