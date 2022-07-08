from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.views import APIView

from georepo.models import Dataset


class IsAllowedAPI(APIView):
    def post(self, request, *args, **kwargs):
        request_url = request.query_params.get('request_url', '')
        try:
            params = list(filter(None, request_url.split('/')))
            dataset_label = params[1]
            entity_type_label = params[2]  # noqa
            cache_key = (
                f'{dataset_label}{request.query_params.get("token", "")}'
            )
            allowed = cache.get(cache_key)
            if allowed is not None:
                if allowed:
                    return HttpResponse('OK')
                else:
                    return HttpResponseForbidden()
            dataset = Dataset.objects.get(
                label=dataset_label
            )
            redis_time_cache = 3600  # seconds
            allowed = request.user.has_perm('view_dataset', dataset)
            cache.set(cache_key, allowed, redis_time_cache)
            if not allowed:
                return HttpResponseForbidden()
        except (IndexError, Dataset.DoesNotExist):
            return HttpResponseForbidden()
        return HttpResponse('OK')
