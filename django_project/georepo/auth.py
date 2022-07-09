from rest_framework.authentication import TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    """
    Customized token based authentication.
    Clients should authenticate by passing the token key in the url.
    For example:
        &token={token_key}
    """

    def authenticate(self, request):
        token = request.GET.get('token', '')
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
        return super(CustomTokenAuthentication, self).authenticate(request)
