from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi




# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="METASQUEEZE API",
        default_version='v1',
        description="API documentation for BITPHYTE - a document conversion platform.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ibehemmanuel32@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)





urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

