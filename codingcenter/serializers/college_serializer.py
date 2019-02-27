from codingcenter.models import College,User
from rest_framework import serializers
from .user_serializer import UserListSerializer

class CollegeDetailSerializer(serializers.Serializer):
    hackerrank_college_id = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        college = College(**validated_data)
        college.save()
        return college

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.hackerrank_college_id =  validated_data.get("hackerrank_college_id", instance.hackerrank_college_id)
        instance.save()
        return instance