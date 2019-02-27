from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from codingcenter.permissions import IsStaffPermission
from codingcenter.serializers import AssignmentListSerializer, AssignmentDetailSerializer, QuestionSerializer
from codingcenter.models import Assignment
from django.http import Http404

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