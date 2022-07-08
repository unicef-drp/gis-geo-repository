from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.views import APIView

from georepo.models import Dataset


class ProtectedApi(APIView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Ok')

    def post(self, request, *args, **kwargs):
        request_url = request.query_params.get('request_url', '')
        try:
            params = list(filter(None, request_url.split('/')))
            dataset_label = params[1]
            entity_type_label = params[2]

            dataset = Dataset.objects.filter(
                label=dataset_label
            )
        except IndexError:
            return HttpResponseForbidden()
        return HttpResponse('Ok')
