from django.contrib import admin
from dashboard.models import (
    LayerFile
)


class LayerFileAdmin(admin.ModelAdmin):
    list_display = ('meta_id', 'upload_date', 'processed', 'layer_file')


admin.site.register(LayerFile, LayerFileAdmin)
