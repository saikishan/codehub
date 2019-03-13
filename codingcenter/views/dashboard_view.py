from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from codingcenter.serializers import DashboardSerializer


class DashboardDataView(APIView):
    def get_dashboard(self, assignment_id, question_id):
        pass
    def get(self, request):
        data = {}  # temp
        if "assignment_id" in request.query_params:
            "get the data based on the assignemnt score board"
            pass
            if "question_id" in request.query_params:
                "get data for the question filter by the assignment"
                pass
        if "question_id" in request.query_params:
            "get data for the question "
            pass
        return Response(data=data, status=status.HTTP_200_OK)
