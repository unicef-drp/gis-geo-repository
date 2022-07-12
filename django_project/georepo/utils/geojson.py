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
        entity_type: EntityType,
        name_field: str,
        dataset: str = None,
        code_field: str = None,
        layer_upload_session_id: str = None) -> bool:
    if not os.path.exists(file_path):
        return False

    entity_added = 0
    entity_updated = 0

    with open(file_path) as json_file:
        data = json.load(json_file)

    upload_session = None
    if layer_upload_session_id:
        from dashboard.models import LayerUploadSession
        upload_session = LayerUploadSession.objects.get(
            id=layer_upload_session_id
        )

    if dataset:
        dataset, _ = Dataset.objects.get_or_create(
            label=dataset
        )

    total_features = len(data['features'])
    index = 1

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
        label = name_field.format(level=level)
        code = code_field.format(level=level)

        if label not in properties or code not in properties:
            continue

        entity, created = GeographicalEntity.objects.update_or_create(
            label=properties[label],
            type=entity_type,
            internal_code=properties[code],
            defaults={
                'geometry': geom,
                'dataset': dataset,
                'level': level,
            }
        )

        if created:
            entity_added += 1
        else:
            entity_updated += 1

        if upload_session:
            upload_session.progress = f'Processing ({index}/{total_features})'
            upload_session.save()

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
                parent_label_field = name_field.format(
                    level=level - 1
                )
                parent_code_field = code_field.format(
                    level=level - 1
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

        index += 1

    if upload_session:
        desc = (
            f'-- {entity_type.label} Entity Type --\n'
            f'{entity_added} {"entity" if entity_added == 1 else "entities"} '
            f'is added\n'
            f'{entity_updated} '
            f'{"entity" if entity_updated == 1 else "entities"} is updated\n\n'

        )
        if not upload_session.message:
            upload_session.message = desc
        else:
            upload_session.message += desc
        upload_session.save()

    return True
