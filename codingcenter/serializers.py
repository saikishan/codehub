from rest_framework import serializers
from codingcenter.models import Assignment,Question,User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'url', 'platform')
        extra_kwargs = {
            'url': {'validators': []},
        }

    def create(self, validated_data):
        obj = Question.objects.create(**validated_data)
        obj.save()
        return obj


class AssignmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    class Meta:
        model = Assignment
        fields = ('id','title','owner','questions')

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        assignment = Assignment.objects.create(**validated_data)
        for question_data in questions_data:
            question, created = Question.objects.get_or_create(url= question_data.pop("url"), defaults=question_data)
            question.assignment_set.add(assignment)
        return assignment

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.owner = validated_data.get("owner", instance.owner)
        questions_data = validated_data.pop('questions')
        if questions_data:
            instance.questions.clear()
            for question_data in questions_data:
                question, created = Question.objects.update_or_create(url= question_data.pop("url"), defaults=question_data)
                instance.questions.add(question)
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','name',)

class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ('username','email','name', 'date_of_birth', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        pass
        #instance.name = validated_data.

