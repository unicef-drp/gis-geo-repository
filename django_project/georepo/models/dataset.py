from django.core.cache import cache
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

        # Clear cache
        cache_keys = cache.get('cache_keys')
        if cache_keys:
            dataset_keys = cache_keys.get('Dataset', [])
            if dataset_keys:
                for dataset_key in dataset_keys:
                    cache.delete(dataset_key)
                    dataset_keys.remove(dataset_key)
                cache_keys['Dataset'] = dataset_keys
                cache.set('cache_keys', cache_keys)

        return super(Dataset, self).save(*args, **kwargs)

    def __str__(self):
        return self.label
