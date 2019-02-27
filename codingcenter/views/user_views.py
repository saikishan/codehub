from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from codingcenter.permissions import IsAdminPermission
from codingcenter.serializers import UserListSerializer,UserDetailSerializer,UserAdminSerializer
from codingcenter.models import User
from django.http import Http404
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

class AdminUserView(APIView):

    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get_object(self,username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, username, format=None):
        user = self.get_object(username)
        user_serialised = UserAdminSerializer(user, data=request.data)
        if user_serialised.is_valid():
            user_serialised.save()
            return Response(user_serialised.data, status=status.HTTP_202_ACCEPTED)
        return Response(user_serialised.errors, status=status.HTTP_400_BAD_REQUEST)