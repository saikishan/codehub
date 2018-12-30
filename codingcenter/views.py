from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.


class AssignmentList(APIView):
    """
    List View to list out all assignments
    #get: return the list of assignemts
    #post: accept the config for the assignemt
    """
    def get(self, request, format = None):

        return Response()

    def post(self, request, format = None):

        return Response()