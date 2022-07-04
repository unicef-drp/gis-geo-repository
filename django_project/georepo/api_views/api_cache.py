import ast

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response


class ApiCache(APIView):
    cache_model = None

    def get_response_data(self, request, *args, **kwargs):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        if ast.literal_eval(
            request.GET.get('cached', 'True')):
            cached_data = self.get_cache()
            if cached_data:
                return Response(cached_data)

        response_data = self.get_response_data(
            request, *args, **kwargs
        )
        self.set_cache(response_data)
        return Response(
            response_data
        )

    def get_cache(self):
        cache_key = (
            f'{self.request.get_full_path()}'
        )
        _cached_data = cache.get(cache_key)
        if _cached_data:
            return _cached_data
        return None

    def set_cache(self, cached_data: dict):
        cache_model_name = f'{self.cache_model.__name__}'
        cache_keys = 'cache_keys'
        cache_keys_data = cache.get(cache_keys)
        cache_key = (
            f'{self.request.get_full_path()}'
        )
        if (
                not cache_keys_data or
                cache_model_name not in cache_keys_data
        ):
            cache_keys_data = {
                cache_model_name: []
            }

        if cache_key not in cache_keys_data[cache_model_name]:
            cache_keys_data[cache_model_name].append(cache_key)

        cache.set(cache_keys, cache_keys_data, None)

        _cached_data = cache.get(cache_key)
        if not _cached_data:
            cache.set(cache_key,
                      cached_data,
                      None)
        else:
            cached_data = _cached_data
        return cached_data
