from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.urls import reverse
from georepo.models import GeographicalEntity


class LevelEntitySerializer(serializers.ModelSerializer):
    level_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = GeographicalEntity

        fields = [
            'level',
            'level_name',
            'url'
        ]

    def get_level_name(self, obj):
        return obj.type.label if obj.type else '-'

    def get_url(self, obj: GeographicalEntity):
        uuid = self.context['uuid'] if 'uuid' in self.context else obj.uuid
        return reverse('reference-layer', kwargs={
            'uuid': uuid,
            'entity_type': self.get_level_name(obj)
        })


class GeographicalEntitySerializer(serializers.ModelSerializer):
    levels = serializers.SerializerMethodField()

    class Meta:
        model = GeographicalEntity
        fields = [
            'label',
            'uuid',
            'source',
            'levels'
        ]

    def get_levels(self, obj: GeographicalEntity):
        all_children = obj.get_all_children()
        levels = []
        entities = []
        for entity in all_children:
            if entity.level not in levels:
                levels.append(entity.level)
                entities.append(entity)
        return LevelEntitySerializer(
            entities,
            context={
              'uuid': obj.uuid
            },
            many=True
        ).data


class GeographicalGeojsonSerializer(GeoFeatureModelSerializer):
    name = serializers.SerializerMethodField()
    level_name = serializers.SerializerMethodField()

    def get_name(self, obj: GeographicalEntity):
        return obj.label

    def get_level_name(self, obj: GeographicalEntity):
        return obj.type.label

    class Meta:
        model = GeographicalEntity
        geo_field = 'geometry'
        fields = [
            'id',
            'name',
            'level_name'
        ]
