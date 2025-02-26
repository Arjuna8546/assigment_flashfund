from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get token from cookie instead of header
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None  # No token, let other auth methods try

        # Validate token
        try:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Invalid or expired token')
        except Exception:
            raise AuthenticationFailed('Authentication failed')