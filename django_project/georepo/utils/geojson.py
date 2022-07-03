import os
import json

from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon

from georepo.models import (
    GeographicalEntity,
    EntityType,
    CodeCL,
    EntityCode,
    Dataset
)


def load_geojson(
        file_path: str,
        level: int,
        name_field: str,
        entity_type: EntityType,
        dataset: str = None,
        code_field: str = None) -> bool:
    if not os.path.exists(file_path):
        return False

    with open(file_path) as json_file:
        data = json.load(json_file)

    if dataset:
        dataset, _ = Dataset.objects.get_or_create(
            label=dataset
        )

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
        label = f'{name_field}'
        code = f'{code_field}'

        if label not in properties or code not in properties:
            continue

        entity, _ = GeographicalEntity.objects.get_or_create(
            label=properties[label],
            type=entity_type,
            internal_code=properties[code],
            defaults={
                'geometry': geom,
                'dataset': dataset,
                'level': level,
            }
        )

        entity.level = level
        entity.save()

        code_cl, _ = CodeCL.objects.get_or_create(
            name='admin'
        )
        EntityCode.objects.get_or_create(
            code_cl=code_cl,
            entity=entity,
            code=properties[code]
        )

        if level > 0:
            try:
                parent_label_field = name_field.replace(
                    f'{level}', f'{level - 1}', 1
                )
                parent_code_field = code_field.replace(
                    f'{level}', f'{level - 1}', 1
                )
                parent = GeographicalEntity.objects.get(
                    label__iexact=properties[parent_label_field],
                    internal_code__iexact=properties[parent_code_field],
                    level=level - 1
                )
                entity.parent = parent
                entity.save()
            except (KeyError, GeographicalEntity.DoesNotExist):
                pass

    return True
