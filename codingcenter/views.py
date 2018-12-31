from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class AssignmentList(APIView):
    """
    List View to list out all assignments
    #get: return the list of assignemts
    #post: accept the config for the assignemt
    """
    def get(self, request, format = None):
        sample_data = [
            {
                "name":"Hack1",
                "owner":"abhinav_dayal",
                "questions_count": 30,
                "status":"active",
            },
            {
                "name": "Hack2",
                "owner": "abhinav_dayal",
                "questions_count": 30,
                "status": "active",
            }
        ]
        return Response(sample_data, status = status.HTTP_200_OK)

    def post(self, request, format = None):

        return Response()