from django.db import models


class Dataset(models.Model):

    label = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )

    vector_tiles_path = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=''
    )

    def __str__(self):
        return self.label
