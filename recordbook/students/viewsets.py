from rest_framework.decorators import action
# from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.forms import model_to_dict

from .models import Student, Group
from .permissions import UserPermission  # IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import StudentSerializer, StudentDetailSerializer
from .utils import StudentAPIPagination
# from rest_framework.permissions import IsAuthenticatedOrReadOnly


class StudentViewSet(viewsets.ModelViewSet):
    pagination_class = StudentAPIPagination
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    permission_classes = (UserPermission, )
    # queryset = Student.objects.all()
    # serializer_class = StudentSerializer

    def get_queryset(self):
        group = self.request.GET.get('group', '')
        if group:
            return Student.objects.filter(group_id=group)
        else:
            return Student.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer

    @action(methods=['get'], detail=False)
    def groups(self, request):
        groups = Group.objects.all()
        return Response({'groups': [f'{gr.course}-{gr.name}' for gr in groups]})

    @action(methods=['get'], detail=True)
    def group(self, request, pk=None):
        group = Group.objects.filter(pk=pk).first()
        if group:
            return Response({'group': f'{group.course}-{group.name}'})
        else:
            return Response({'group': 'Группа не найдена'})

# class StudentAPIView(ListCreateAPIView):
#    queryset = Student.objects.all()
#    serializer_class = StudentSerializer
    # def get(self, request):
    #    #return Response({'first_name': 'Alexander'})
    #    st = Student.objects.all().values()
    #    return Response({'students': list(st)})

    # def post(self, request):
    #    return Response({'first_name': 'Nastya'})

# class StudentAPIDetailView(RetrieveUpdateDestroyAPIView):
#    queryset = Student.objects.all()
#    serializer_class = StudentSerializer


class GroupAPIView(APIView):
    def get(self, request):
        gr = Group.objects.all().values()
        return Response({'groups': list(gr)})

    def post(self, request):
        new_gr = Group.objects.create(
            name=request.data['name'],
            course=request.data['course'],
            enrollment_year=request.data['enrollment_year']
        )
        return Response({'group': model_to_dict(new_gr)})
