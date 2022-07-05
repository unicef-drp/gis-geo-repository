import math

from rest_framework.generics import get_object_or_404
from django.core.paginator import Paginator

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
        page = int(request.GET.get('page', '1'))
        page_size = int(request.GET.get('page_size', '50'))

        try:
            entity_layer = GeographicalEntity.objects.get(
                uuid=uuid
            )
        except GeographicalEntity.DoesNotExist:
            return []

        dataset = entity_layer.dataset
        entities = GeographicalEntity.objects.filter(
            dataset=dataset
        )
        if entity_type:
            entities = entities.filter(
                type__label=entity_type
            )

        paginator = Paginator(entities, page_size)
        total_page = math.ceil(paginator.count / page_size)
        if page > total_page:
            output = []
        else:
            paginated_entities = paginator.get_page(page)
            output = (
                self.get_serializer()(
                    paginated_entities, many=True).data
            )
        return {
            'page': page,
            'total_page': total_page,
            'page_size': page_size,
            'results': output
        }


class ReferenceLayerGeojson(ReferenceLayerEntityList):
    """
    Reference Layer in Geojson.
    """
    def get_serializer(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return GeographicalGeojsonSerializer
