from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from codingcenter.serializers import  AssignmentSerializer
from codingcenter.models import Assignment
# Create your views here.


class AssignmentListView(APIView):
    """
    List View to list out all assignments
    #get: return the list of assignemts
    #post: accept the config for the assignemt
    """
    def get(self, request, format = None):

        return Response(AssignmentSerializer(Assignment.objects.all() ,many= True).data , status = status.HTTP_200_OK)

    def post(self, request, format = None):
        assignmentserialised = AssignmentSerializer(data=request.data)
        if assignmentserialised.is_valid():
            assignmentserialised.save()
            return Response(assignmentserialised.data, status= status.HTTP_201_CREATED)
        return Response(assignmentserialised.errors , status= status.HTTP_400_BAD_REQUEST)

