from rest_framework import serializers
from codingcenter.models import Assignment,Question

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