from django.contrib import admin
from dashboard.models import (
    LayerFile,
    LayerUploadSession
)


class LayerFileAdmin(admin.ModelAdmin):
    list_display = ('meta_id', 'upload_date', 'processed', 'layer_file')


@admin.action(description='Load layer files to database')
def load_layer_files(modeladmin, request, queryset):
    from dashboard.tasks import process_layer_upload_session
    for upload_session in queryset:
        process_layer_upload_session.delay(upload_session.id)


class LayerUploadSessionAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'status', 'started_at', 'modified_at')
    actions = [load_layer_files]


admin.site.register(LayerFile, LayerFileAdmin)
admin.site.register(LayerUploadSession, LayerUploadSessionAdmin)
