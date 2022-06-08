from rest_framework.response import Response
from rest_framework.views import APIView

from georepo.models import GeographicalEntity
from georepo.serializers.entity import GeographicalGeojsonSerializer


class ReferenceLayer(APIView):
    """
    Reference Layer in Geojson.
    """
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
            GeographicalGeojsonSerializer(entities, many=True).data
        )

        return Response(geojson_output)
