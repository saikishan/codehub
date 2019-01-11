from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from codingcenter.serializers import  AssignmentSerializer, QuestionSerializer, UserListSerializer, UserDetailSerializer
from django.http import Http404
from codingcenter.models import Assignment,Question,User
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
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

class UserListView(APIView):
    def get(self, request, format):
        return  UserListSerializer(User.objects.all,many=True)

    def post(self, request, format=None):
        userserialised = UserListSerializer(data=request.data)
        if userserialised.is_valid():
            userserialised.save()
            return Response(userserialised.data, status=status.HTTP_201_CREATED)
        return Response(userserialised.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        user = self.get_object(username)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, username, format=None):
        user = self.get_object(username)
        if request.user != user and request.user.is_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_serialised = UserListSerializer(user, data=request)
        if user_serialised.is_valid():
            user_serialised.save()
            return Response(user_serialised.data, status=status.HTTP_202_ACCEPTED)
        return Response(user_serialised.errors, status=status.HTTP_400_BAD_REQUEST)



