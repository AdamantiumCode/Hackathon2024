"""
Модуль отвечающий за отрисовку страниц для пользователя.
И Подготовки данных для отображения на страницах 
"""
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore

from .forms import LocationForm
from .models import QuestRoom, Answer, Location, Service, ServiceTag


def home_page(request):
    """
    Начальная страница

    Аргументы:
        request (_type_): _Запрос от пользователя_
    """
    return render(request, "game/home.html")


def view_services_page(request):
    """
    Страница со всеми услугами

    Аргументы:
        request (_type_): _Запрос от пользователя_
    """
    all_services = Service.objects.all()
    
    context = {
        "services": all_services,
    }
    
    return render(request, "game/all_services.html", context=context)


def select_location_page(request):
    """
    Страница с выбором местности для поиска услуги

    Аргументы:
        request (_type_): _Запрос от пользователя_
    """
    if request.method == "POST":
        location = request.POST.get("location")
        request.session["location"] = location # Запись в сессию местоположения пользователя
        
        quest_room = QuestRoom.objects.filter(name="Земля")[0]
        return redirect("quest_room", pk=quest_room.id)

    form = LocationForm() # Выпадающий список
    all_locations = Location.objects.all()
    
    context = {
        "form": form,
        "locations": all_locations,
    }
    
    return render(request, "game/location.html", context)


def quest_room_page(request, pk):
    """
    Страница с комнатами для вопросов

    Аргументы:
        request (_type_): _Запрос от пользователя_.
        pk (_type_): _Уникальное значение, связывает страницу и комнату с вопросами_.
    """
    quest_room = QuestRoom.objects.get(id=pk)

    if request.method == "POST":
        new_pk, answer = request.POST.get("answer").split("_")
        
        # Если ключ от несуществующей комнаты, то редирект
        if new_pk == 0:
            return redirect("result")
        
        # Запись ответа пользователя
        request.session[f"answers{pk}"] = answer
        
        return redirect("quest_room", pk=new_pk)
    
    # Проверка валидности ответов и вопросов у комнаты
    # Костыльненько, но мера предосторожности
    question = quest_room.question
    
    if question is None:
        return redirect("result")
    
    answers = Answer.objects.filter(question__id=question.id)
    
    if answers.count() == 0:
        return redirect("result")
    
    # Формирование списка следующий вопросов
    next_quests = QuestRoom.objects.filter(parent_room__id=quest_room.id)
    
    #  Создание невалидных ссылок, если вопросов нет
    if next_quests.count() == 0:
        next_quests = [0] * answers.count()

    context = {
        "question": question,
        "data": zip(answers, next_quests),
        "parent": quest_room.parent_room,
    }
    
    return render(request, "game/quest_room.html", context)


def result_page(request):
    """
    Страница с результатами ответов на вопросы - списком услуг

    Аргументы:
        request (_type_): _Запрос от пользователя_
    """
    
    # Получение сессии пользователя, для работы с его ответами
    user_session = SessionStore(session_key=request.session.session_key)
    
    # Критерии для фильтрации услуг
    location = "--Неважно--"
    answers = []
    
    # Получение критериев из сессии пользователя
    for key, value in user_session.items():
        if key == "location":
            location = value
            
        elif "answer" in key:
            answers.append(value)
    
    # Сортировка по местоположению
    all_services = Service.objects.all().filter(
        Q(location__name__contains=location) | Q(location__name="--Неважно--")
    )
    
    # Формирование списка подходящих услуг
    result_services = []
    
    for service in all_services:
        all_tags = ServiceTag.objects.filter(service=service)
        
        filtered_service_tags = all_tags.filter(
            Q(answer__name__in=answers) | Q(answer__name__icontains="Неважно")
        )

        # Если все теги у услуги совпали с пользовательскими, то она подходит
        if all_tags.count() == filtered_service_tags.count():
            result_services.append(service)

    # Пересоздание сессии
    user_session.flush()
    request.session.create()
    
    context = {
        "services": result_services,
    }
    
    return render(request, "game/result.html", context)
