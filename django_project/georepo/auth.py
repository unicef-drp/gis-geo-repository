from oauth2_provider.models import AccessToken
from oauth2_provider.contrib.rest_framework import OAuth2Authentication


class CustomTokenAuthentication(OAuth2Authentication):

    def authenticate_header(self, request):
        return None

    def authenticate(self, request):
        token = request.GET.get('token', '')
        if token:
            access_token = AccessToken.objects.get(token=token)
            request.auth = access_token
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        return super(CustomTokenAuthentication, self).authenticate(request)
