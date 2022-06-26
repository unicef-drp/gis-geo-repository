from georepo.api_views.api_cache import ApiCache
from georepo.models import GeographicalEntity, Dataset
from georepo.serializers.entity import EntitySerializer


class ReferenceLayerList(ApiCache):
    """
    View to list all reference layers in the system
    """
    cache_model = Dataset

    def get_response_data(self, request, *args, **kwargs):
        parent_entities = GeographicalEntity.objects.filter(
            parent__isnull=True
        )
        serializer = EntitySerializer(
            parent_entities,
            many=True
        )
        return serializer.data
