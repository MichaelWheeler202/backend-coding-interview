from django.db import models

class Photographer(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, auto_created=False)
    photographer = models.CharField(max_length=255)
    photographer_url = models.URLField(null=True)

    class Meta:
        db_table = "photographers"

class Photo(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True, auto_created=False)
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    url = models.URLField()
    photographer_id = models.ForeignKey(Photographer, on_delete=models.CASCADE, help_text="ID of photographer if available", null=True)
    avg_color = models.CharField(max_length=255, null=True)
    src_original = models.URLField()
    src_large2x = models.URLField(null=True)
    src_large = models.URLField(null=True)
    src_medium = models.URLField(null=True)
    src_small = models.URLField(null=True)
    src_portrait = models.URLField(null=True)
    src_landscape = models.URLField(null=True)
    src_tiny = models.URLField(null=True)
    alt = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "photos"

