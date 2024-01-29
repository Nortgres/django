from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.http import HttpResponse
from django.views.generic import ListView

from .forms import AddStudentForm
from .models import Student

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Студенты", 'url_name': 'students'},
        {'title': "Преподаватели", 'url_name': 'teachers'},
        {'title': "Войти", 'url_name': 'login'}]

##def index(request):
    #return HttpResponse("Страница приложения students.")
##    students = Student.objects.all()
##    context = {
##        'students': students,
##        'menu': menu,
##        'title': 'Главная страница'
##    }
##    return render(request, 'students/index.html', context=context)
    #return render(request, 'students/index.html', {'students': students, 'menu': menu, 'title': 'Главная страница'})
def groups(request, group):
    if request.GET:
        print(request.GET)
    #if request.POST:
    #    print(request.POST)
    return HttpResponse(f"<h1>Список студентов по группам.\
                        </h1><h2>{group}</h2>")

def about(request):
    return render(request, 'students/about.html', {'menu': menu, 'title': 'О сайте'})

def students(request):
    return HttpResponse("Студенты")

def teachers(request):
    return HttpResponse("Преподаватели")

def login(request):
    return HttpResponse("Авторизация")

def show_student(request, stud_slug):
    #return HttpResponse(f"Отображение студента с id = {stud_id}")
    student = get_object_or_404(Student, slug=stud_slug)

    context = {
        'st': student,
        'menu': menu,
    }
    return render(request, 'students/student.html', context=context)

def addstudent(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
                #try:
                    #Student.objects.create(**form.cleaned_data)
                    form.save()
                    return redirect('home')
                #except:
                #    form.add_error(None, 'Ошибка!')
    else:
        form = AddStudentForm()
    return render(request, 'students/addstudent.html', {'form': form})

class StudentHome(ListView):
    model = Student
    template_name = 'students/index.html'
    context_object_name = 'students'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        return context

    def get_queryset(self):
        return Student.objects.filter(is_study=True)