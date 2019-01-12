from rest_framework.views import APIView
from codingcenter.models import Assignment,Question
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class AssignmentJoinView(APIView):
    def get_object(self,pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404


class QuestionRedirectView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,pk):
        try:
            return Question.objects.get(id=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        if not question.has_user(request.user):
            question.participants.add(request.user)
            question.save()
        return Response({ "url" :question.url })
