from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminPermission,IsStaffPermission
from codingcenter.serializers import  (AssignmentListSerializer,AssignmentDetailSerializer,
                                       QuestionSerializer,
                                       UserListSerializer, UserDetailSerializer,UserAdminSerializer)
from django.http import Http404
from codingcenter.models import Assignment,Question,User
# Create your views here.

class AssignmentJoinView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        assignment = self.get_object(pk)
        assignment.participants.add(request.user)
        assignment.save()
        return Response(status=status.HTTP_200_OK)

class AssignmentListView(APIView):
    """
    List View to list out all assignments
    #get: return the list of assignemts
    #post: accept the config for the assignemt
    """
    permission_classes = [IsAuthenticated,]# IsStaffPermission]
    def get(self, request, format = None):
        return Response(AssignmentListSerializer(Assignment.objects.all() ,many= True).data , status = status.HTTP_200_OK)

    def post(self, request, format = None):
        assignmentserialised = AssignmentDetailSerializer(data=request.data, context={
            'request' : request,
        })
        if assignmentserialised.is_valid():
            assignmentserialised.save()
            return Response(assignmentserialised.data, status= status.HTTP_201_CREATED)
        return Response(assignmentserialised.errors , status= status.HTTP_400_BAD_REQUEST)

class AssignmentDetailView(APIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
    def get_object(self, pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404

    def put(self,request ,pk, format=None):
        assignment = self.get_object(pk)
        serializer = AssignmentListSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        assignment = self.get_object(pk)
        serializer = AssignmentDetailSerializer(assignment)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        assignment = self.get_object(pk)
        return Response(status= status.HTTP_200_OK)

class QuestionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsStaffPermission]
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
    def get(self, request, format=None):
        return  Response(UserListSerializer(User.objects.all(),many=True).data)

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

class QuestionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        return Response(QuestionSerializer(Question.objects.all(), many=True).data, status= status.HTTP_200_OK)

class AssignmentQuestionsView(APIView):
    def get_object(self,pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        assignment = self.get_object(pk)
        questionserialised = QuestionSerializer(assignment.questions, many=True)
        return Response(questionserialised.data,status=200)

    def post(self, request, pk, format=None):
        assignment = self.get_object(pk)
        question_serialised = QuestionSerializer(data= request.data, context={
            "request" : request
        })
        if question_serialised.is_valid():
            question = question_serialised.save()
            assignment.questions.add(question)
            assignment.save()
            return Response(question_serialised.data, status=status.HTTP_201_CREATED)
        return Response(question_serialised.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format):
        assignment = self.get_object(pk)



class AdminUserView(APIView):

    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get_object(self,username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, username, format=None):
        user = user = self.get_object(username)
        user_serialised = UserListSerializer(user, data=request)
        if user_serialised.is_valid():
            user_serialised.save()
            return Response(user_serialised.data, status=status.HTTP_202_ACCEPTED)
