import os

from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

# from dashboard.models.layer_file import LayerFile


class LayerUploadView(APIView):
     parser_classes = (MultiPartParser, )

     def post(self, request, format=None):
          file_obj = request.FILES['file']
          # layer_file, _ = LayerFile.objects.get_or_create(
          #      name=file_obj.name,
          #      uploader=self.request.user
          # )
          # layer_file.layer_file = file_obj
          # layer_file.meta_id = request.POST.get('id', '')
          # layer_file.save()
          if isinstance(file_obj, TemporaryUploadedFile):
               if os.path.exists(file_obj.temporary_file_path()):
                    os.remove(file_obj.temporary_file_path())
          return Response(status=204)


class LayersProcessView(APIView):
     def post(self, request, format=None):
          all_layers = request.POST.get('allFiles', '')
          return Response(status=200)
