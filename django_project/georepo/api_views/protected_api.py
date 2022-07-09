from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from georepo.auth import CustomTokenAuthentication
from georepo.models import Dataset


class IsDatasetAllowedAPI(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def has_perm(self, user, permission: str, dataset: Dataset) -> bool:
        return user.has_perm(permission, dataset)

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
            allowed = self.has_perm(self.request.user, 'view_dataset', dataset)
            cache.set(cache_key, allowed, redis_time_cache)
            if not allowed:
                return HttpResponseForbidden()
        except (IndexError, Dataset.DoesNotExist):
            return HttpResponseForbidden()
        return HttpResponse('OK')
