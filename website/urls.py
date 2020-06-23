from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # /admin/
    path('admin/', admin.site.urls),

    # /
    path('', include('tutorial.urls', namespace='tutorial')),

    # / accounts/
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # / settings/
    path('settings/', include('settings.urls', namespace='settings')),
]
