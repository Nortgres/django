from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from .models import Student

menu = ["О сайте", "Студенты", "Преподаватели", "Войти"]

def index(request):
    #return HttpResponse("Страница приложения students.")
    students = Student.objects.all()
    return render(request, 'students/index.html', {'students': students, 'menu': menu, 'title': 'Главная страница'})
def groups(request, group):
    if request.GET:
        print(request.GET)
    #if request.POST:
    #    print(request.POST)
    return HttpResponse(f"<h1>Список студентов по группам.\
                        </h1><h2>{group}</h2>")

def about(request):
    return render(request, 'students/about.html', {'menu': menu, 'title': 'О сайте'})