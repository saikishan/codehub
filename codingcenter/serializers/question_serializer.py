from rest_framework import serializers
from codingcenter.models import Question
from .user_serializer import UserListSerializer

class QuestionSerializer(serializers.ModelSerializer):
    created_by = UserListSerializer(required=False)
    class Meta:
        model = Question
        fields = ('id', 'url', 'created_by')
        extra_kwargs = {
            'url': {'validators': []},
        }
    def _user(self):
        return self.context["request"].user

    def create(self, question_data):
        question_data["created_by"] = self._user()
        question, created = Question.objects.get_or_create(url= question_data.pop("url"), defaults=question_data)
        return question