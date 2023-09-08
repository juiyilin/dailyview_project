from django.urls import path, include, re_path
import os

urlpatterns = [
    path('api/', include('api.urls')),
]
# if os.environ.get('DJANGO_SETTINGS_MODULE') != 'project.deploy':
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='',
        description="""
        """,
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('test/', TestView.as_view()),
]
if os.environ.get('DJANGO_SETTINGS_MODULE') != 'project.deploy':
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
