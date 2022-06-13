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
        code_field: str = None,
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
        label = f'admin{level}{name_field}'
        code = f'admin{level}{code_field}'

        if dataset:
            dataset, _ = Dataset.objects.get_or_create(
                label=dataset
            )

        entity, _ = GeographicalEntity.objects.get_or_create(
            label=properties[label],
            level=level,
            type=entity_type,
            defaults={
                'geometry': geom,
                'dataset': dataset,
            }
        )

        if code:
            code_cl, _ = CodeCL.objects.get_or_create(
                name='admin'
            )
            EntityCode.objects.get_or_create(
                code_cl=code_cl,
                entity=entity,
                code=properties[code]
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
