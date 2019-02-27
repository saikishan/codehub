from .question_serializer import QuestionSerializer
from .user_serializer import UserListSerializer
from rest_framework import serializers
from codingcenter.models import Assignment,Question,User

class AssignmentListSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False, write_only=True)
    created_by = UserListSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ('id','title','questions',"created_by")



class AssignmentDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)
    created_by = UserListSerializer(read_only=True)
    def _user(self):
        return self.context["request"].user

    class Meta:
        model = Assignment
        fields = ('id','title','questions',"created_by")


    def create(self, validated_data):
        questions_data = validated_data.pop('questions',[])
        assignment = Assignment.objects.create(created_by=self._user(), **validated_data)
        for question_data in questions_data:
            question, created = Question.objects.get_or_create(url= question_data.pop("url"), defaults=question_data)
            question.assignment_set.add(assignment)
        return assignment

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        questions_data = validated_data.pop('questions')
        if questions_data:
            instance.questions.clear()
            for question_data in questions_data:
                question, created = Question.objects.update_or_create(url= question_data.pop("url"), defaults=question_data)
                instance.questions.add(question)
        instance.save()
        return instance


