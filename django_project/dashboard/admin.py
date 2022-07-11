from django.contrib import admin
from dashboard.models import (
    LayerFile,
    LayerUploadSession
)


class LayerFileAdmin(admin.ModelAdmin):
    list_display = ('meta_id', 'upload_date', 'processed', 'layer_file')


class LayerUploadSessionAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'status', 'started_at', 'modified_at')


admin.site.register(LayerFile, LayerFileAdmin)
admin.site.register(LayerUploadSession, LayerUploadSessionAdmin)
