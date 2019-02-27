from rest_framework import serializers
from codingcenter.models import User
class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    hackerrank_id = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username','email','name', 'password', "is_admin", "is_staff", "date_of_birth", "hackerrank_id")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.username = validated_data.get("username", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.hackerrank_id = validated_data.get("hackerrank_id", instance.hackerrank_id)
        instance.save()
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ('username','email','name',"is_admin","is_staff")

class UserAdminSerializer(serializers.ModelSerializer):
    is_admin =  serializers.BooleanField(required=False)
    is_admin = serializers.BooleanField(required=False)
    class Meta:
        model = User
        fields = ('is_admin', 'is_staff')

    def update(self, instance, validated_data):
        instance.is_admin = validated_data.get("is_admin", instance.is_admin)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.save()
        return instance