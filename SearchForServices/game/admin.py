from django.contrib import admin

from .models import Service, Location, Answer, ServiceTag, Question, QuestRoom


# Основные модели
admin.site.register(Service)
admin.site.register(Location)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(QuestRoom)

# Вспомогательные
admin.site.register(ServiceTag)
