from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from .filters import StudentFilter
from .forms import AddStudentForm, RegisterUserForm, LoginUserForm, FilterStudentForm
from .models import Student
from .utils import menu, DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin

#menu = [{'title': "О сайте", 'url_name': 'about'},
#        {'title': "Студенты", 'url_name': 'students'},
#        {'title': "Преподаватели", 'url_name': 'teachers'},
#        {'title': "Войти", 'url_name': 'login'}]

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

#def login(request):
#    return HttpResponse("Авторизация")

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

class StudentHome(DataMixin, ListView):
    model = Student
    template_name = 'students/index.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user.is_authenticated
        queryset = self.get_queryset()
        st_filter = StudentFilter(self.request.GET, queryset)
        #c_def = self.get_user_context(title='Главная страница', auth=auth, form=FilterStudentForm(self.request.GET))
        c_def = self.get_user_context(title='Главная страница', auth=auth, st_filter=st_filter)
        return {**context, **c_def}

    def get_queryset(self):
        queryset = super().get_queryset()
        st_filter = StudentFilter(self.request.GET, queryset)
        return st_filter.qs
        #filters = {}
        #first_name = self.request.GET.get('first_name')
        #last_name = self.request.GET.get('last_name')
        #group = self.request.GET.get('group')
        #if first_name:
        #    filters['first_name__contains'] = first_name  #__contains - содержит
        #if last_name:
        #    filters['last_name__contains'] = last_name
        #if group:
        #    filters['group'] = group
        #new_context = Student.objects.filter(**filters)
        #return new_context

class ShowStudent(DataMixin, DetailView):
    model = Student
    template_name = 'students/student.html'
    slug_url_kwarg = 'stud_slug'
    context_object_name = 'st'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user.is_authenticated
        c_def = self.get_user_context(title='Главная страница', auth=auth)
        return {**context, **c_def}
class AddStudent(LoginRequiredMixin, CreateView):
    form_class = AddStudentForm
    template_name = 'students/addstudent.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'students/register.html'
    success_url = reverse_lazy('login')
    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'students/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return {**context, **c_def}
    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

class DeleteStudent(LoginRequiredMixin, DataMixin, DeleteView):
    model = Student
    template_name = 'student/delete_student.html'
    success_url = reverse_lazy('home')
    context_object_name = 'st'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Удалить студента')
        return {**context, **c_def}