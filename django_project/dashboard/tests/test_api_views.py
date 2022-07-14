
import mock
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIRequestFactory

from dashboard.api_views.layer_upload import (
    LayerUploadView,
    LayerRemoveView,
    LayersProcessView,
    LayerProcessStatusView
)
from dashboard.models import LayerFile, LayerUploadSession, PROCESSING
from dashboard.tests.model_factories import LayerFileF, LayerUploadSessionF
from georepo.tests.model_factories import UserF


class DummyTask:
    def __init__(self, id):
        self.id = id


def mocked_process_layer_upload_session(*args, **kwargs):
    return DummyTask('1')


class TestApiViews(TestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_layer_upload(self):
        file = SimpleUploadedFile(
            'admin.geojson',
            b'file_content',
            content_type='application/geo+json')
        request = self.factory.post(
            reverse('layer-upload'), {
                'id': 'layer-id',
                'file': file
            }
        )
        request.user = UserF.create()
        view = LayerUploadView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 204)
        self.assertTrue(LayerFile.objects.filter(
            name='admin.geojson',
            meta_id='layer-id'
        ).exists())

    def test_layer_process_status(self):
        upload_session = LayerUploadSessionF.create()
        request = self.factory.get(
            reverse('layers-process-status') + (
                f'?session_id={upload_session.id}'
            )
        )
        user = UserF.create(username='test')
        request.user = user
        view = LayerProcessStatusView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(
            reverse('layers-process-status')
        )
        request.user = user
        response = view(request)
        self.assertEqual(response.status_code, 404)

        request = self.factory.get(
            reverse('layers-process-status') + (
                '?session_id=9999'
            )
        )
        request.user = user
        view = LayerProcessStatusView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 404)

    def test_remove_layer(self):
        layer_file = LayerFileF.create()
        request = self.factory.post(
            reverse('layer-remove'), {
                'meta_id': layer_file.meta_id,
            }
        )
        request.user = UserF.create(username='test')
        view = LayerRemoveView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            LayerFile.objects.filter(meta_id=layer_file.meta_id).exists())

    @mock.patch(
        'dashboard.api_views.layer_upload.process_layer_upload_session.delay',
        mock.Mock(side_effect=mocked_process_layer_upload_session))
    def test_process_layers(self):
        uploader = UserF.create(username='uploader')
        layer_file_1 = LayerFileF.create(
            meta_id='test_1',
            uploader=uploader)
        layer_file_2 = LayerFileF.create(meta_id='test_2', uploader=uploader)
        post_data = {
            'entity_types': {
                layer_file_1.meta_id: 'Country',
                layer_file_2.meta_id: 'Region'
            },
            'levels': {
                layer_file_1.meta_id: '0',
                layer_file_2.meta_id: '1'
            },
            'all_files': [
                {
                    'id': layer_file_1.meta_id,
                },
                {
                    'id': layer_file_2.meta_id,
                }
            ],
            'dataset': 'dataset_name',
            'code_format': 'code_{level}',
            'label_format': 'admin_{level}'
        }
        request = self.factory.post(
            reverse('layers-process'), post_data,
            format='json'
        )
        request.user = UserF.create(username='test')
        view = LayersProcessView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            LayerUploadSession.objects.filter(
                dataset='dataset_name',
                status=PROCESSING
            ).exists()
        )
