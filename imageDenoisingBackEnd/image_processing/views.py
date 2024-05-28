from rest_framework import viewsets
from rest_framework.response import Response
from .models import Image
from .serializers import ImageSerializer
from rest_framework.decorators import action

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_noise(self, request, pk=None):
        image = self.get_object()
        noise_type = request.data.get('selected_noise')
        # Add noise logic here
        # Update the noise type in the image instance
        image.selected_noise = noise_type
        image.save()
        return Response({'status': 'noise added', 'noise': noise_type})
