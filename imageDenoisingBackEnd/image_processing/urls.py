from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet

router = DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('images/denoise/', ImageViewSet.as_view({'post': 'denoise'}), name='image-denoise'),
]
