from rest_framework.permissions import DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class FullDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self) -> None:
        # Adjust the permissions map for GET to match 'view' permissions
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

    def has_permission(self, request, view):
        # Ensure that the user is authenticated via JWT
        if not request.user or not request.user.is_authenticated:
            return False
        # Use the base permissions to check the model-level permissions
        return super().has_permission(request, view)
