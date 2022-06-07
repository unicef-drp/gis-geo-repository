from rest_framework.response import Response
from rest_framework.views import APIView
from georepo.models import GeographicalEntity
from georepo.serializers.entity import GeographicalEntitySerializer


class ReferenceLayerList(APIView):
    """
    View to list all reference layers in the system
    """

    def get(self, request, format=None) -> Response:
        parent_entities = GeographicalEntity.objects.filter(
            parent__isnull=True
        )
        serializer = GeographicalEntitySerializer(
            parent_entities,
            many=True
        )
        return Response(serializer.data)
