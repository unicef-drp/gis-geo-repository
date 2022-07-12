import factory

from dashboard.models import (
    LayerFile,
    LayerUploadSession
)
from georepo.tests.model_factories import UserF


class LayerUploadSessionF(factory.django.DjangoModelFactory):
    class Meta:
        model = LayerUploadSession

    dataset = factory.Sequence(
        lambda n: u'dataset %s' % n
    )


class LayerFileF(factory.django.DjangoModelFactory):
    class Meta:
        model = LayerFile

    meta_id = factory.Sequence(
        lambda n: u'meta_id_%s' % n
    )

    layer_file = factory.django.FileField(filename='admin.geojson')

    name = factory.Sequence(
        lambda n: u'name %s' % n
    )

    level = factory.Sequence(
        lambda n: u'level %s' % n
    )

    entity_type = factory.Sequence(
        lambda n: u'entity type %s' % n
    )

    layer_upload_session = factory.SubFactory(
        LayerUploadSessionF
    )

    uploader = factory.SubFactory(UserF)
