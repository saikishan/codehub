from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from codingcenter.models import Assignment,Question

class DashboardDataView(APIView):
    def get_dashboard(self, assignment_id, question_id):
        pass
    def get(self, request):
        data = {}  # temp
        if "assignment_id" in request.query_params:
            current_assignment = Assignment.objects.get(id= request.query_params["assignment_id"])
            if "question_id" in request.query_params:
                data = current_assignment.get_dashboard(question_id=request.query_params["question_id"])
            else:
                data = current_assignment.get_dashboard()
            return Response(data=data, status=status.HTTP_200_OK)
        if "question_id" in request.query_params:
            current_question = Question.objects.get(id = request.query_params["question_id"])
            data = current_question.get_dashboard()
        return Response(data=data, status=status.HTTP_200_OK)
