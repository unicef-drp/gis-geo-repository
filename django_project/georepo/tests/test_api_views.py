import uuid

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory

from georepo.api_views.reference_layer import (
    ReferenceLayerDetail,
    ReferenceLayerEntityList
)
from georepo.tests.model_factories import (
    GeographicalEntityF, EntityTypeF, DatasetF
)


class TestApiViews(TestCase):

    def setUp(self) -> None:
        self.entity_type = EntityTypeF.create(label='Country')
        self.dataset = DatasetF.create()
        self.entity = GeographicalEntityF.create(
            uuid=str(uuid.uuid4()),
            type=self.entity_type,
            level=0,
            dataset=self.dataset
        )
        self.factory = APIRequestFactory()

    def test_get_reference_layer_detail(self):
        kwargs = {
            'uuid': self.entity.uuid
        }
        request = self.factory.get(
            reverse('reference-layer-detail', kwargs=kwargs)
        )
        view = ReferenceLayerDetail.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_get_reference_layer_list(self):
        entity_type = EntityTypeF.create(label='District')
        GeographicalEntityF.create(
            uuid=str(uuid.uuid4()),
            type=entity_type,
            level=1,
            dataset=self.dataset
        )
        kwargs = {
            'uuid': self.entity.uuid,
            'entity_type': entity_type
        }
        request = self.factory.get(
            reverse('reference-layer-list')
        )
        view = ReferenceLayerEntityList.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
