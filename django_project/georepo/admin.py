from django.contrib import admin
from georepo.models import (
    GeographicalEntity,
    Language,
    EntityType,
    EntityName
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


admin.site.register(GeographicalEntity, GeographicalEntityAdmin)
admin.site.register(Language)
admin.site.register(EntityType)
admin.site.register(EntityName)
