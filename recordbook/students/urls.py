# from django.contrib import admin
from django.urls import path, include
from .views import groups, about, students, teachers, StudentHome, \
    ShowStudent, AddStudent, RegisterUser, LoginUser, logout_user, \
    DeleteStudent, UpdateStudent, Gradebook, AddMark \
    # login, show_student, addstudent,
from .viewsets import StudentViewSet, GroupAPIView \
    # StudentAPIView,  StudentAPIDetailView,
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')
# router.register(r'groups', GroupAPIView, basename='groups')

urlpatterns = [
    path('about/', about, name='about'),
    path('students/', students, name='students'),
    # path('student/<slug:stud_slug>/', show_student, name='student'),
    path('student/<slug:stud_slug>/', ShowStudent.as_view(), name='student'),
    path('teachers/', teachers, name='teachers'),
    path('login/', LoginUser.as_view(), name='login'),
    path('groups/<slug:group>/', groups),
    # path('addstudent/', addstudent, name='addstudent'),
    path('addstudent/', AddStudent.as_view(), name='addstudent'),
    # path('', index, name='home'),
    path('', StudentHome.as_view(), name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('student/<int:pk>/delete/', DeleteStudent.as_view(), name="delete_student"),
    path('student/<int:pk>/update/', UpdateStudent.as_view(), name="update_student"),
    path('gradebook/', Gradebook.as_view(), name='gradebook'),
    path('addmark/', AddMark.as_view(), name='addmark'),
    # path('api/v1/students/', StudentAPIView.as_view()),
    # path('api/v1/student/<int:pk>/', StudentAPIDetailView.as_view()),
    path('api/v1/groups/', GroupAPIView.as_view()),
    # path('api/v1/students/', StudentViewSet.as_view({'get': 'list'})),
    # path('api/v1/student/<int:pk>/', StudentViewSet.as_view({'put': 'update'})),
    path('api/v1/', include(router.urls))
]
