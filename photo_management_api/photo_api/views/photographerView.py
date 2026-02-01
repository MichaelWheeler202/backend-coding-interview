from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from ..models import Photographer
from ..serializer import PhotographerSerializer
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

class PhotographerView(APIView):

    @extend_schema(
        request=None,
        responses=PhotographerSerializer
    )
    def get(self, request, photographerId: int):
        """
        Retrieve a Photographer by their ID.
        """
        logger.info(f"Received request to get photographer {photographerId}")
        if photographerId <= 0:
            logger.info(f"Invalid ID entered {photographerId}")
            return Response({"error": "Positive Integer for ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            photographer = Photographer.objects.get(pk=photographerId)
        except ObjectDoesNotExist:
            logger.info(f"Photographer ID {photographerId} not found.")
            return Response({"error": f"Photographer ID {photographerId} not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PhotographerSerializer(photographer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses=None
    )
    def delete(self, request, photographerId: int):
        """
        Delete a Photographer by their ID.
        """
        logger.info(f"Received request to delete photographer {photographerId}")
        if photographerId <= 0:
            logger.info(f"Invalid ID entered {photographerId}")
            return Response({"error": "Positive Integer for ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Photographer.objects.get(pk=photographerId).delete()
        except ObjectDoesNotExist:
            logger.info(f"Photographer ID {photographerId} not found.")
            return Response({"error": f"Photographer ID {photographerId} not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        request=PhotographerSerializer,
        responses=None
    )
    def post(self, request):
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
            Photographer.objects.create(**photographer.validated_data)
        except IntegrityError as e:
            logger.error(f"IntegrityError when creating photographer: {e}")
            return Response({"error": "Photographer with this ID already exists or data violates constraints."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error when creating photographer: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)


