from collections import OrderedDict
from uuid import UUID

import mock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from georepo.api_views.reference_layer_list import ReferenceLayerList
from georepo.tests.model_factories import *  # noqa


def mocked_cache_get(self, *args, **kwargs):
    return OrderedDict(
        [('name', 'entity 0'),
         ('identifier', UUID('4685e7fe-5996-48aa-9e56-98820f53a7b2'))]
    )


class TestApiCache(TestCase):

    def setUp(self) -> None:
        self.view = ReferenceLayerList.as_view()
        self.entity = GeographicalEntityF.create()
        self.factory = APIRequestFactory()
        self.request = self.factory.get(
            reverse('reference-layer-list')
        )


    @mock.patch('django.core.cache.cache.get',
                mock.Mock(side_effect=mocked_cache_get))
    def test_get_cache(self):
        response = self.view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.entity.label, 'entity 0')


    def test_get_without_cache(self):
        response = self.view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.entity.label, response.data[0].get('name'))
