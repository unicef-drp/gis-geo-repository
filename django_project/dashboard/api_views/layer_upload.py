import os

from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.models import (
    LayerFile,
    LayerUploadSession, PENDING, PROCESSING
)
from dashboard.tasks import process_layer_upload_session


class LayerProcessStatusView(APIView):
    def get(self, request):
        session_id = request.GET.get('session_id')
        if not session_id:
            return Response(status=404)
        try:
            upload_session = LayerUploadSession.objects.get(
                id=session_id
            )
        except LayerUploadSession.DoesNotExist:
            return Response(status=404)
        return Response(
            status=200,
            data={
                'status': upload_session.status,
                'progress': upload_session.progress,
                'message': upload_session.message
            }
        )


class LayerUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file_obj = request.FILES['file']
        layer_file, _ = LayerFile.objects.get_or_create(
            name=file_obj.name,
            uploader=self.request.user
        )
        layer_file.layer_file = file_obj
        layer_file.meta_id = request.POST.get('id', '')
        layer_file.save()
        if isinstance(file_obj, TemporaryUploadedFile):
            if os.path.exists(file_obj.temporary_file_path()):
                os.remove(file_obj.temporary_file_path())
        return Response(status=204)


class LayerRemoveView(APIView):
    def post(self, request, format=None):
        file_meta_id = request.data.get('meta_id')
        layer_file = LayerFile.objects.get(
            meta_id=file_meta_id
        )
        layer_file.delete()
        return Response(status=200)


class LayersProcessView(APIView):
    """
    Example of POST request payload :
    {
         'entity_types': {
              'id-file-1': 'Country',
              'id-file-2': 'Region'
         },
         'levels': {
             'id-file-1': '0',
             'id-file-2': '1'
         },
         'all_files': [
         {
               'name': 'file_name',
               'size': 74823,
               'type': 'image/png',
               'lastModifiedDate': '2019-09-26T08:16:22.706Z',
               'uploadedDate': '2022-07-12T03:07:58.077Z',
               'percent': 100,
               'id': 'id-file-1',
               'status': 'done',
               'previewUrl': 'blob:...',
               'width': 1043,
               'height': 521
         },...
         ],
         'dataset': 'dataset_name',
         'code_format': 'code_{level}',
         'label_format': 'admin_{level}'
    }
    """

    def post(self, request, format=None):
        entity_types = request.data.get('entity_types', {})
        levels = request.data.get('levels', {})
        all_files = request.data.get('all_files', [])
        dataset = request.data.get('dataset', '')
        code_format = request.data.get('code_format', '')
        label_format = request.data.get('label_format', '')

        layer_upload_session, _ = LayerUploadSession.objects.get_or_create(
            dataset=dataset,
            layer_code_format=code_format,
            layer_name_format=label_format,
            status=PENDING
        )

        for layer_file in all_files:
            layer_file_obj = LayerFile.objects.get(
                meta_id=layer_file['id']
            )
            entity_type = entity_types.get(layer_file_obj.meta_id, '')
            level = levels.get(layer_file_obj.meta_id, '')
            layer_file_obj.layer_upload_session = layer_upload_session
            layer_file_obj.entity_type = entity_type
            layer_file_obj.level = level
            layer_file_obj.save()

        layer_upload_session.status = PROCESSING
        layer_upload_session.progress = ''
        layer_upload_session.message = ''

        task = process_layer_upload_session.delay(layer_upload_session.id)

        layer_upload_session.task_id = task.id
        layer_upload_session.save()

        return Response(status=200, data={
            'message': layer_upload_session.message,
            'layer_upload_session_id': layer_upload_session.id
        })
