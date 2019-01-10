from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from codingcenter.serializers import  AssignmentSerializer,QuestionSerializer
from django.http import Http404
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

class AssignmentDetailView(APIView):
    def get_object(self, pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404

    def put(self,request ,pk, format=None):
        assignment = self.get_object(pk)
        serializer = AssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        assignment = self.get_object(pk)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        assignment = self.get_object(pk)
        return Response(status= status.HTTP_200_OK)

class QuestionDetailView(APIView):
    def get_object(self, pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
