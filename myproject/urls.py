from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define schema view for Swagger API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API documentation for our project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@ourapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Combine all URL patterns into one list
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('api/', include('products.urls')),  # API URLs from the 'products' app
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),  # Swagger docs
]
