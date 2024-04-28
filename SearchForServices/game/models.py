from django.db import models


class Service(models.Model):
    """
    Модель Услуг для сайта
    """
    # Основная характеристика услуги
    name = models.CharField(max_length=120, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created = models.DateField(auto_now=True)
    updated = models.DateField(auto_now_add=True)

    # Данные для поиска
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    service_tags = models.ManyToManyField("Answer", through="ServiceTag")

    def __str__(self) -> str:
        return self.name


class Location(models.Model):
    """
    Модель для создания районов и регионов
    """
    name = models.CharField(max_length=120, null=True, blank=True)
    
    class Meta:
        ordering = ["-name"]

    def __str__(self) -> str:
        return self.name


class Answer(models.Model):
    """
    Ответ на вопрос для комнаты
    """
    name = models.CharField(max_length=120, null=False, blank=False)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class ServiceTag(models.Model):
    """
    Промежуточный тег для связи  услуги и ответа, который подходит для нее
    """
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)


class Question(models.Model):
    """
    Вопрос для компанты
    """
    description = models.TextField(null=False, blank=False)

    image = models.ImageField(null=True, blank=True, default="quest_logo.svg")

    def __str__(self) -> str:
        return self.description


class QuestRoom(models.Model):
    """
    Комната содержащая вопрос, связывающая ответ, вопросы на него и следующие комнаты 
    При выборе i-ого варианта ответа на вопрос, будет выбрана i-ая комната с вопросом
    """
    name = models.CharField(max_length=120, null=False, blank=False)
    parent_room = models.ForeignKey("QuestRoom", on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(
        "Question", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name
