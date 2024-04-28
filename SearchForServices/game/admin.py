from django.contrib import admin

from .models import Service, Location, Answer, ServiceTag, Question, QuestRoom


# Добавления возможности редактирования моделей для БД из админки
admin.site.register(Service)
admin.site.register(Location)
admin.site.register(Answer)
admin.site.register(Question)

admin.site.register(QuestRoom)
admin.site.register(ServiceTag)
