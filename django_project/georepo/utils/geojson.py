import os
import json

from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon

from georepo.models import GeographicalEntity, EntityType


def load_geojson(
        file_path: str,
        level: int,
        name_field: str,
        entity_type: EntityType,
        parent_field: str = None) -> bool:
    if not os.path.exists(file_path):
        return False

    with open(file_path) as json_file:
        data = json.load(json_file)

    for feature in data['features']:
        geom_str = json.dumps(feature['geometry'])
        properties = feature['properties']
        geom = GEOSGeometry(geom_str)
        if isinstance(geom, Polygon):
            geom = MultiPolygon([geom])
        if not isinstance(geom, MultiPolygon):
            raise TypeError(
                'Type is not acceptable'
            )
        entity, _ = GeographicalEntity.objects.get_or_create(
            label=properties[name_field],
            level=level,
            type=entity_type,
            defaults={
                'geometry': geom
            }
        )
        if parent_field:
            try:
                parent = GeographicalEntity.objects.get(
                    label__iexact=properties[parent_field],
                    level=level - 1
                )
                entity.parent = parent
                entity.save()
            except (KeyError, GeographicalEntity.DoesNotExist):
                pass

    return True