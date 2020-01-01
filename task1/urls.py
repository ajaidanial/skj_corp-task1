from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", view=admin.site.urls, name="admin urls"),
    path("app/", view=include("main_app.urls"), name="main_app urls"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
