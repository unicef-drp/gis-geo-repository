from django.http import HttpResponse
from rest_framework.views import APIView


class ProtectedApi(APIView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Ok')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Ok')
