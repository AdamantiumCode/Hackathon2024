from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Ссылки для сервисов сайта
    path("admin/", admin.site.urls),
    path("", include('game.urls')),
    
    # Обращение к API
    path("api/", include("game.api.urls"))
]
