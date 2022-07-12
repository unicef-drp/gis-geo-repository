from django.contrib import admin
from dashboard.models import (
    LayerFile,
    LayerUploadSession, DONE, PROCESSING
)
from georepo.models import EntityType


class LayerFileAdmin(admin.ModelAdmin):
    list_display = ('meta_id', 'upload_date', 'processed', 'layer_file')


@admin.action(description='Load layer files to database')
def load_layer_files(modeladmin, request, queryset):
    from georepo.utils.geojson import load_geojson
    for upload_session in queryset:
        upload_session.status = PROCESSING
        upload_session.progress = ''
        upload_session.message = ''
        upload_session.save()
        for layer_file in upload_session.layerfile_set.all().order_by('level'):
            entity_type, _ = EntityType.objects.get_or_create(
                label=layer_file.entity_type
            )
            load_geojson(
                layer_file.layer_file.path,
                int(layer_file.level),
                entity_type,
                upload_session.layer_name_format,
                upload_session.dataset,
                upload_session.layer_code_format,
                upload_session.id
            )
            layer_file.processed = True
            layer_file.save()
        LayerUploadSession.objects.filter(id=upload_session.id).update(
            status=DONE
        )


class LayerUploadSessionAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'status', 'started_at', 'modified_at')
    actions = [load_layer_files]


admin.site.register(LayerFile, LayerFileAdmin)
admin.site.register(LayerUploadSession, LayerUploadSessionAdmin)
