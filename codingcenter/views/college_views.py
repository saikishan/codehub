from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from codingcenter.permissions import IsStaffPermission
from codingcenter.serializers import CollegeDetailSerializer
from codingcenter.models import College
from django.http import Http404

class CollegeListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        colleges = CollegeDetailSerializer(College.objects.all(), many=True)
        return Response(colleges.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        college_serialised = CollegeDetailSerializer(data=request.data)
        if college_serialised.is_valid():
            college_serialised.save()
            return Response(college_serialised.data, status=status.HTTP_201_CREATED)
        return Response(college_serialised.errors, status=status.HTTP_400_BAD_REQUEST)