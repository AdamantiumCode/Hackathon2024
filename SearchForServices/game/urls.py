from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_page, name="home"),
    path("location/", views.location_page, name="location"),
    path("quest_room/<str:pk>/", views.quest_room_page, name="quest_room"),
    path("result/", views.result_page, name="result"),
]
