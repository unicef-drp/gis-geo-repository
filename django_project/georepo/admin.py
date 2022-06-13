from django.contrib import admin
from georepo.models import (
    GeographicalEntity,
    Language,
    EntityType,
    EntityName,
    Dataset
)


class GeographicalEntityAdmin(admin.ModelAdmin):
    list_display = (
        'label', 'level', 'type'
    )
    list_filter = (
        'level', 'type'
    )
    search_fields = (
        'label',
    )

    def get_queryset(self, request):
        return GeographicalEntity.objects.filter(id__gte=0)


@admin.action(description='Generate vector tiles')
def generate_vector_tiles(modeladmin, request, queryset):
    from georepo.utils.vector_tile import generate_vector_tiles
    for dataset in queryset:
        generate_vector_tiles(dataset, True)


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('label', )
    actions = [generate_vector_tiles]


admin.site.register(GeographicalEntity, GeographicalEntityAdmin)
admin.site.register(Language)
admin.site.register(EntityType)
admin.site.register(EntityName)
admin.site.register(Dataset, DatasetAdmin)
