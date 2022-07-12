from django.db import models

DONE = 'Done'
PENDING = 'Pending'
CANCELED = 'Canceled'
PROCESSING = 'Processing'
ERROR = 'Error'


class LayerUploadSession(models.Model):
    STATUS_CHOICES = (
        (DONE, DONE),
        (PENDING, PENDING),
        (CANCELED, CANCELED),
        (ERROR, ERROR),
        (PROCESSING, PROCESSING)
    )

    dataset = models.CharField(
        blank=False,
        null=False,
        max_length=256
    )

    layer_name_format = models.CharField(
        blank=False,
        null=False,
        max_length=256
    )

    layer_code_format = models.CharField(
        blank=False,
        null=False,
        max_length=256
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        auto_now=True
    )

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=128,
        null=False,
        blank=False
    )

    message = models.TextField(
        null=True,
        blank=True
    )

    progress = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.dataset} - {self.status}'
