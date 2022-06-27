import factory

from georepo.models import (
    Dataset,
    GeographicalEntity,
    EntityType
)


class DatasetF(factory.django.DjangoModelFactory):
    class Meta:
        model = Dataset

    label = factory.Sequence(
        lambda n: u'dataset %s' % n
    )


class EntityTypeF(factory.django.DjangoModelFactory):
    class Meta:
        model = EntityType

    label = factory.Sequence(
        lambda n: u'entity type %s' % n
    )


class GeographicalEntityF(factory.django.DjangoModelFactory):
    class Meta:
        model = GeographicalEntity

    dataset = factory.SubFactory(DatasetF)

    label = factory.Sequence(
        lambda n: u'entity %s' % n
    )

    type = factory.SubFactory(EntityTypeF)
