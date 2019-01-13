from rest_framework import serializers
from codingcenter.models import Assignment,Question,User

class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ('username','email','name', 'password', "is_admin", "is_staff", "date_of_birth")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.username = validated_data.get("username", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)

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
        return instance

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
        return instance


