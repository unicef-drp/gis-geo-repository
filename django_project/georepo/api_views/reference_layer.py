from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from georepo.models import GeographicalEntity
from georepo.serializers.entity import (
    GeographicalGeojsonSerializer,
    GeographicalEntitySerializer,
    DetailedEntitySerializer
)


class ReferenceLayerDetail(APIView):
    """
    API to get reference layer detail
    """
    def get(self, request, uuid=None, *args, **kwargs):
        entity_layer = get_object_or_404(
            GeographicalEntity, uuid=uuid
        )
        return Response(
            DetailedEntitySerializer(entity_layer).data
        )


class ReferenceLayerEntityList(APIView):
    """
    Reference layer list per entity type
    """

    def get_serializer(self):
        return GeographicalEntitySerializer

    def get(self, request, uuid=None, entity_type=None, *args, **kwargs):
        try:
            entity_layer = GeographicalEntity.objects.get(
                uuid=uuid
            )
        except GeographicalEntity.DoesNotExist:
            return Response([])

        all_children = entity_layer.get_all_children()
        entities = []
        for children in all_children:
            if children.type.label == entity_type:
                entities.append(children)

        geojson_output = (
            self.get_serializer()(entities, many=True).data
        )

        return Response(geojson_output)


class ReferenceLayerGeojson(ReferenceLayerEntityList):
    """
    Reference Layer in Geojson.
    """
    def get_serializer(self):
        return GeographicalGeojsonSerializer
