from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms import model_to_dict

from .models import Student, Group
from .serializers import StudentSerializer


#class StudentAPIView(ListAPIView):
#    queryset = Student.objects.all()
#    serializer_class = StudentSerializer

class StudentAPIView(APIView):
    def get(self, request):
        #return Response({'first_name': 'Alexander'})
        st = Student.objects.all().values()
        return Response({'students': list(st)})

    def post(self, request):
        return Response({'first_name': 'Nastya'})

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