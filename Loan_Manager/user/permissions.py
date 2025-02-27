from rest_framework.permissions import BasePermission
from .authenticate import CookieJWTAuthentication

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        
        authenticator = CookieJWTAuthentication()
        try:

            user,token = authenticator.authenticate(request)

            return token.get('role') == 'admin'
        except:
            return False