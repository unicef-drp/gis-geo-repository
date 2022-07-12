
import mock
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIRequestFactory

from dashboard.api_views.layer_upload import (
    LayerUploadView,
    LayerRemoveView,
    LayersProcessView
)
from dashboard.models import LayerFile, LayerUploadSession, DONE
from dashboard.tests.model_factories import LayerFileF
from georepo.tests.model_factories import UserF


def mocked_load_geojson_success(*args, **kwargs):
    return True, ''


def mocked_load_geojson_error(*args, **kwargs):
    return False, 'Error'


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

    @mock.patch('dashboard.api_views.layer_upload.load_geojson',
                mock.Mock(side_effect=mocked_load_geojson_success))
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
            LayerFile.objects.get(id=layer_file_1.id).processed)
        self.assertTrue(
            LayerUploadSession.objects.filter(
                dataset='dataset_name',
                status=DONE
            ).exists()
        )

    @mock.patch('dashboard.api_views.layer_upload.load_geojson',
                mock.Mock(side_effect=mocked_load_geojson_error))
    def test_process_layers_failed(self):
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
        self.assertEqual(response.status_code, 400)
