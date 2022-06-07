from rest_framework import serializers
from georepo.models import GeographicalEntity


class LevelEntitySerializer(serializers.ModelSerializer):
    level_name = serializers.SerializerMethodField()

    class Meta:
        model = GeographicalEntity
        fields = [
            'level',
            'level_name'
        ]

    def get_level_name(self, obj):
        return obj.type.label if obj.type else '-'


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

    def get_levels(self, obj):
        all_children = obj.get_all_children()
        levels = []
        entities = []
        for entity in all_children:
            if entity.level not in levels:
                levels.append(entity.level)
                entities.append(entity)
        return LevelEntitySerializer(entities, many=True).data
