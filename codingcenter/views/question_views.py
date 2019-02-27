from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from codingcenter.permissions import IsStaffPermission
from codingcenter.serializers import QuestionSerializer
from codingcenter.models import Question
from django.http import Http404

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

class QuestionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        return Response(QuestionSerializer(Question.objects.all(), many=True).data, status= status.HTTP_200_OK)
