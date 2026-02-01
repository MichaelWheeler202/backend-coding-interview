from django.urls import path

from .views import PhotoView, PhotographerView

urlpatterns = [
    path('photos/', PhotoView.as_view(http_method_names=['post']), name='photo'),
    path('photos/<int:photoId>/', PhotoView.as_view(http_method_names=['get', 'delete']), name='photo'),

    path('photographers/', PhotographerView.as_view(http_method_names=['post']), name='photographer'),
    path('photographers/<int:photographerId>/', PhotographerView.as_view(http_method_names=['get', 'delete']), name='photographer'),
]