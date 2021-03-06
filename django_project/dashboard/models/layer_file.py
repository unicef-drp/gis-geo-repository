from django.db import models
from django.conf import settings


class LayerFile(models.Model):
    id = models.AutoField(primary_key=True)

    meta_id = models.CharField(
        blank=True,
        default='',
        max_length=256
    )

    upload_date = models.DateTimeField(
        null=True,
        blank=True
    )

    layer_file = models.FileField(
        upload_to='layer_files/%Y/%m/%d/'
    )

    processed = models.BooleanField(
        default=False
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        default='',
        blank=True,
        max_length=512
    )

    level = models.CharField(
        default='',
        blank=True,
        max_length=128
    )

    entity_type = models.CharField(
        default='',
        blank=True,
        max_length=256
    )

    layer_upload_session = models.ForeignKey(
        'dashboard.LayerUploadSession',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
