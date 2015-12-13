from rest_framework.authentication import SessionAuthentication as OriginalSessionAuthentication


class UnsafeSessionAuthentication(OriginalSessionAuthentication):

    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, 'user', None)

        if not user or not user.is_active:
           return None

        return (user, None)


class NoCsrfSessionAuthentication(OriginalSessionAuthentication):
    def enforce_csrf(self, request):
        return

