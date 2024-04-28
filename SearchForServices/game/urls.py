from django.urls import path
from . import views


# Привязка адресов и функций отрисовки страниц
urlpatterns = [
    path("", views.home_page, name="home"),
    path("all_services", views.view_services_page, name="all_services"),
    path("location/", views.select_location_page, name="location"),
    path("quest_room/<str:pk>/", views.quest_room_page, name="quest_room"),
    path("result/", views.result_page, name="result"),
]
