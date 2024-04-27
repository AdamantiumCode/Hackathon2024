from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import QuestRoom, Question, Answer, Location, Service, ServiceTag
from .forms import LocationForm


def home_page(request):
    return render(request, "game/home.html")

def location_page(request):
    if request.method == "POST":
        location = request.POST.get("location")
        request.session["location"] = location
        
        return redirect("quest_room", pk=1)

    form = LocationForm()
    locations = Location.objects.all().order_by("name")
        
    context = {
        "form": form,
        "locations": locations,
    }
    
    return render(request, "game/location.html", context)


def quest_room_page(request, pk):
    print(pk)
    quest_room = QuestRoom.objects.get(id=pk)

    if request.method == "POST":
        new_pk, answer = request.POST.get("answer").split("_")
        
        if new_pk == 0:
            return redirect("result")
        request.session[f"answers{pk}"] = answer
        
        return redirect("quest_room", pk=new_pk)
    
    question = quest_room.question
    if question is None:
        return redirect("result")
    answers = Answer.objects.filter(question__id=question.id)
    
    if answers.count() == 0:
        return redirect("result")
    
    next_quests = QuestRoom.objects.filter(parent_room__id=quest_room.id)
    
    if next_quests.count() == 0:
        next_quests = [0] * answers.count()

    context = {
        "question": question,
        "data": zip(answers, next_quests),
        "parent": quest_room.parent_room,
    }
    return render(request, "game/quest_room.html", context)


def result_page(request):
    session = SessionStore(session_key=request.session.session_key)
    
    location = None
    answers = []
    
    for key, value in session.items():
        if key == "location":
            location = value
        elif "answer" in key:
            answers.append(value)

    session.flush()
    request.session.create()
    
    # Сортировка по местоположению
    services = Service.objects.all().filter(
        Q(location__name__contains=location) |
        Q(location__name="Неважно")
    )
    
    result_services = []
    
    for service in services:
        all_service_tags = ServiceTag.objects.filter(
            service=service
        )
        filtered_service_tags = all_service_tags.filter(
            Q(answer__name__in=answers) |
            Q(answer__name__icontains="Неважно")
        )
        
        if all_service_tags.count() == filtered_service_tags.count():
            result_services.append(service)
    
    context = {
        "services": result_services
    }
    
    return render(request, "game/result.html", context)
