from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from user.views import obtain_auth_token
from user.forms import AdminAuthenticationForm
from .api import router, urls

schema_view = get_schema_view(
   openapi.Info(
      title="Test tasl api",
      default_version='v1',
      description="Test task for alente",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = 'Администрирование календаря мероприятий'
admin.site.login_form = AdminAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/auth', obtain_auth_token),
    path('v1/', include(router.urls)),
    path('v1/', include(urls)),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
