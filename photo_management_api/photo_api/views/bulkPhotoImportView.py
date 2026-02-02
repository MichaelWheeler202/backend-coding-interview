import io

from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status

from ..models import Photo, Photographer
from ..serializer import PhotographerSerializer, PhotoSerializer
import logging

import csv

logger = logging.getLogger(__name__)

class BulkPhotoImportView(APIView):


    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "csv": {"type": "string", "format": "binary"}},
            },
        },
        responses=None
    )
    def post(self, request):
        """
        Import photos (and photographers) from a CSV payload. CSV columns like photos.csv are supported.
        Accepts an uploaded file (any field) or raw CSV in the request body.
        """
        logger.info("Importing Photos and Authors by CSV")

        file = request.FILES["csv"]
        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        io_string.seek(0)
        reader = csv.DictReader(io_string, delimiter=',')
        reader.fieldnames = [name.replace('.', '_') for name in reader.fieldnames]

        photoSerializers = []
        photographerSerializers = []

        for row in reader:
            try:
                photographer_id = int(row.get("photographer_id"))
                if not Photographer.objects.filter(pk=photographer_id).exists():
                    logger.info(f"Adding photographer Id {photographer_id}")
                    photographerSerializers.append(PhotographerSerializer(data={"id": photographer_id, "photographer": row.get("photographer"), "photographer_url": row.get("photographer_url")}))
                else:
                    logger.info(f"Skipping duplicate photographer Id {photographer_id}")

                photo_id = int(row.get("id") )
                if not Photo.objects.filter(pk=photo_id).exists():
                    logger.info(f"Adding photo Id {photo_id}")
                    photoSerializers.append(PhotoSerializer(data=row))

                else:
                    logger.info(f"Skipping duplicate photo Id {photo_id}")
            except Exception as e:
                logger.error(f"Exception parsing row: {e}")

        photographers = []
        for s in photographerSerializers:
            if s.is_valid():
                photographer = Photographer(**s.validated_data)
                photographers.append(photographer)
            else:
                logger.error(f"Invalid photographer data {s.errors}")
        Photographer.objects.bulk_create(photographers)

        photos = []
        for s in photoSerializers:
            if s.is_valid():
                photo = Photo(**s.validated_data)
                photos.append(photo)
            else:
                logger.error(f"Invalid photo data {s.errors}")
        Photo.objects.bulk_create(photos)

        return Response(status=status.HTTP_201_CREATED)
