from rest_framework.views import APIView
from codingcenter.models import Assignment,Question,Result
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

    def get(self, request, id, format=None):
        question = self.get_object(id)
        if(Result.objects.filter(question = question, user= request.user).count() == 0):
            re = Result(question = question, user= request.user)
            re.save()
        return Response({ "url" :question.url })
