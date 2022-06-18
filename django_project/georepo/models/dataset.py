from django.db import models
from django.utils import timezone


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

    last_update = models.DateTimeField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        self.last_update = timezone.now()
        return super(Dataset, self).save(*args, **kwargs)

    def __str__(self):
        return self.label
