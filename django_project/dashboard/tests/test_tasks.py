from django.test import TestCase
from django.urls import reverse
from mock import mock
from rest_framework.test import APIRequestFactory

from dashboard.api_views.layer_upload import LayersProcessView
from dashboard.models import LayerUploadSession, DONE, ERROR
from dashboard.tests.model_factories import LayerFileF
from dashboard.tests.test_api_views import mocked_process_layer_upload_session
from dashboard.tasks import process_layer_upload_session
from georepo.tests.model_factories import UserF


def mocked_load_geojson_error(*args, **kwargs):
    return False, 'Error'


def mocked_load_geojson_success(*args, **kwargs):
    return True, ''


class TestTasks(TestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    @mock.patch(
        'dashboard.api_views.layer_upload.process_layer_upload_session.delay',
        mock.Mock(side_effect=mocked_process_layer_upload_session))
    @mock.patch('dashboard.tasks.load_geojson',
                mock.Mock(side_effect=mocked_load_geojson_success))
    def test_process_layer_upload_session_task_success(self):
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

        upload_session = LayerUploadSession.objects.get(
            dataset='dataset_name',
        )
        process_layer_upload_session(upload_session.id)
        self.assertTrue(
            LayerUploadSession.objects.get(
                dataset='dataset_name'
            ).status == DONE
        )

    @mock.patch(
        'dashboard.api_views.layer_upload.process_layer_upload_session.delay',
        mock.Mock(side_effect=mocked_process_layer_upload_session))
    @mock.patch('dashboard.tasks.load_geojson',
                mock.Mock(side_effect=mocked_load_geojson_error))
    def test_process_layer_upload_session_task_error(self):
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

        upload_session = LayerUploadSession.objects.get(
            dataset='dataset_name',
        )
        process_layer_upload_session(upload_session.id)
        self.assertTrue(
            LayerUploadSession.objects.get(
                dataset='dataset_name'
            ).status == ERROR
        )
