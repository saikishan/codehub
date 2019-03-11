from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    status = serializers.BooleanField(required=False)
    count = serializers.IntegerField(required=False)