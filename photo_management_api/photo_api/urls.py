from django.urls import path
from .views import get_photo, get_photographer, create_photographer, delete_photographer, delete_photo, create_photo
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('photo/<int:photoId>', get_photo, name='get_photo'),
    path('photo', create_photo, name='create_photo'),
    path('photo/<int:photoId>', delete_photo, name='delete_photo'),

    path('photographer/<int:photographerId>', get_photographer, name='get_photographer'),
    path('photographer', create_photographer, name='create_photographer'),
    path('photographer/<int:photoId>', delete_photographer, name='delete_photographer'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]