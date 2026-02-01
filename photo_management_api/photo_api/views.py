from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Photo
from .serializer import PhotoSerializer
from .models import Photographer
from .serializer import PhotographerSerializer
import logging
from django.db import IntegrityError

logger = logging.getLogger(__name__)

@extend_schema(
    request=None,
    responses=PhotoSerializer
)
@api_view(['GET'])
def get_photo(request, photoId: int):
    """
    Retrieve a photo by its ID.
    """
    logger.info(f"Received request to get photo {photoId}")
    if photoId <= 0:
        logger.info(f"Invalid ID entered {photoId}")
        return Response({"error": "Positive Integer for ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        photo = Photo.objects.get(id=photoId)
    except ObjectDoesNotExist:
        logger.info(f"Photo ID {photoId} does not exist")
        return Response({f"Photo ID {photoId} does not exist"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PhotoSerializer(photo)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=None,
    responses=None
)
@api_view(['DELETE'])
def delete_photo(request, photoId: int):
    """
    Retrieve a photo by its ID.
    """
    logger.info(f"Received request to delete photo {photoId}")
    if photoId <= 0:
        logger.info(f"Invalid ID entered {photoId}")
        return Response({"error": "Positive Integer for ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        photo = Photo.objects.delete(id=photoId)
    except ObjectDoesNotExist:
        logger.info(f"Photo ID {photoId} does not exist")
        return Response({"error": f"Photo ID {photoId} does not exist"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PhotoSerializer(photo)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    request=PhotoSerializer,
    responses=None
)
@api_view(['POST'])
def create_photo(request):
    """
    Create a new Photographer.

    Expects JSON body matching PhotographerSerializer (fields: id, photographer, photographer_url).
    """
    logger.info(f"Received request to create photo {request.data}")
    photo = PhotoSerializer(data=request.data)
    if not photo.is_valid():
        logger.info(f"Photographer creation validation failed: {photo.errors}")
        return Response(photo.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        Photographer.objects.create(photo)
    except IntegrityError as e:
        logger.error(f"IntegrityError when creating photographer: {e}")
        return Response({"error": "Photographer with this ID already exists or data violates constraints."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error when creating photographer: {e}")
        return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_201_CREATED)


@extend_schema(
    request=None,
    responses=PhotographerSerializer
)
@api_view(['GET'])
def get_photographer(request, photographerId: int):
    """
    Retrieve a Photographer by their ID.
    """
    logger.info(f"Received request to get photographer {photographerId}")
    if photographerId <= 0:
        logger.info(f"Invalid ID entered {photographerId}")
        return Response({"error": "Positive Integer for ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        photographer = Photographer.objects.get(id=photographerId)
    except ObjectDoesNotExist:
        logger.info(f"Photographer ID {photographerId} not found.")
        return Response({"error": f"Photographer ID {photographerId} not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PhotographerSerializer(photographer)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    request=None,
    responses=None
)
@api_view(['DELETE'])
def delete_photographer(request, photographerId: int):
    """
    Retrieve a Photographer by their ID.
    """
    logger.info(f"Received request to delete photographer {photographerId}")
    if photographerId <= 0:
        logger.info(f"Invalid ID entered {photographerId}")
        return Response({"error": "Positive Integer for ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        photographer = Photographer.objects.delete(id=photographerId)
    except ObjectDoesNotExist:
        logger.info(f"Photographer ID {photographerId} not found.")
        return Response({"error": f"Photographer ID {photographerId} not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_200_OK)

@extend_schema(
    request=PhotographerSerializer,
    responses=None
)
@api_view(['POST'])
def create_photographer(request):
    """
    Create a new Photographer.
    Expects JSON body matching PhotographerSerializer (fields: id, photographer, photographer_url).
    """
    logger.info(f"Received request to create photographer {request.data}")
    photographer = PhotographerSerializer(data=request.data)
    if not photographer.is_valid():
        logger.error(f"Photographer creation validation failed: {photographer.errors}")
        return Response(photographer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        Photographer.objects.create(photographer)
    except IntegrityError as e:
        logger.error(f"IntegrityError when creating photographer: {e}")
        return Response({"error": "Photographer with this ID already exists or data violates constraints."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error when creating photographer: {e}")
        return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_201_CREATED)
