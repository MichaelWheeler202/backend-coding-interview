from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status

from ..models import Photo
from ..serializer import PhotoSerializer
import logging
from django.db import IntegrityError

logger = logging.getLogger(__name__)

class PhotoView(APIView):

    @extend_schema(
        request=None,
        responses=PhotoSerializer
    )
    def get(self, request, photoId: int):
        """
        Retrieve a photo by its ID.
        """
        logger.info(f"Received request to get photo {photoId}")
        if photoId <= 0:
            logger.info(f"Invalid ID entered {photoId}")
            return Response({"error": "Positive Integer for ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            photo = Photo.objects.get(pk=photoId)
        except ObjectDoesNotExist:
            logger.info(f"Photo ID {photoId} does not exist")
            return Response({"error": f"Photo ID {photoId} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PhotoSerializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        request=None,
        responses=None
    )
    def delete(self, request, photoId: int):
        """
        Delete a photo by its ID.
        """
        logger.info(f"Received request to delete photo {photoId}")
        if photoId <= 0:
            logger.info(f"Invalid ID entered {photoId}")
            return Response({"error": "Positive Integer for ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Photo.objects.get(pk=photoId).delete()
        except ObjectDoesNotExist:
            logger.info(f"Photo ID {photoId} does not exist.")
            return Response({"error": f"Photo ID {photoId} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        request=PhotoSerializer,
        responses=None
    )
    def post(self, request):
        """
        Create a new Photo.
        """
        logger.info(f"Received request to create photo {request.data}")
        photo = PhotoSerializer(data=request.data)
        if not photo.is_valid() :
            logger.info(f"Photo creation validation failed: {photo.errors}")
            return Response(photo.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            Photo.objects.create(**photo.validated_data)
        except IntegrityError as e:
            logger.error(f"IntegrityError when creating photo: {e}")
            return Response({"error": "Photo with this ID already exists or data violates constraints."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error when creating photo: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)




