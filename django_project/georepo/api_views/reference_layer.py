from rest_framework.generics import get_object_or_404

from georepo.api_views.api_cache import ApiCache
from georepo.models import GeographicalEntity, Dataset
from georepo.serializers.entity import (
    GeographicalGeojsonSerializer,
    GeographicalEntitySerializer,
    DetailedEntitySerializer
)


class ReferenceLayerDetail(ApiCache):
    """
    API to get reference layer detail
    """
    cache_model = Dataset

    def get_response_data(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid', None)
        entity_layer = get_object_or_404(
            GeographicalEntity, uuid=uuid
        )
        response_data = (
            DetailedEntitySerializer(entity_layer).data
        )
        return response_data


class ReferenceLayerEntityList(ApiCache):
    """
    Reference layer list per entity type
    """
    cache_model = Dataset

    def get_serializer(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return GeographicalEntitySerializer

    def get_response_data(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid', None)
        entity_type = kwargs.get('entity_type', None)
        try:
            entity_layer = GeographicalEntity.objects.get(
                uuid=uuid
            )
        except GeographicalEntity.DoesNotExist:
            return []

        all_children = entity_layer.get_all_children()
        entities = []
        for children in all_children:
            if children.type.label == entity_type:
                entities.append(children)

        geojson_output = (
            self.get_serializer()(entities, many=True).data
        )
        return geojson_output


class ReferenceLayerGeojson(ReferenceLayerEntityList):
    """
    Reference Layer in Geojson.
    """
    def get_serializer(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return GeographicalGeojsonSerializer
