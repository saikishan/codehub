from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

#custom user models dont touch
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, username,  date_of_birth, password):
        user = self.model(
            email =  email,
            date_of_birth = date_of_birth,
            name = name,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staffuser(self, email, name, username, date_of_birth, password):
        user = self.create_user(
            email = email,
            name = name ,
            date_of_birth = date_of_birth,
            username= username
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_adminuser(self, email, name, username, date_of_birth, password):
        user = self.create_user(
            email = email,
            name = name ,
            date_of_birth = date_of_birth,
            username= username
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    objects = UserManager()
    email = models.EmailField(verbose_name='email address',
                    max_length=255,
                    unique=True,)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    hackerrank_id = models.CharField(max_length=30, unique=True, default=None, null=True)
    description = models.CharField(default="Explain Yourself!", max_length=500)
    questions = models.ManyToManyField("Question", through="Result")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'name', 'username']

    def __str__(self):
        return self.email

class Question(models.Model):
    title = models.CharField(max_length= 30)
    url = models.CharField(max_length= 100, unique= True)
    created_by = models.ForeignKey('codingcenter.User', related_name='created_questions', null=True, on_delete=models.SET_NULL)
    participants = models.ManyToManyField("User", through="Result")
    def has_user(self,user):
        return True if Question.objects.filter(id=self.id, solved_by__in = [user]).count() == 1 else False

class Assignment(models.Model):
    title = models.CharField(max_length=20)
    created_by = models.ForeignKey('codingcenter.User',related_name= 'created_assignments', null=True, on_delete=models.SET_NULL)
    questions = models.ManyToManyField(Question)
    def has_user(self, user):
        return True if (Assignment.objects.filter(id=self.id, participants_id = user.id).count() == 1) else False


class College(models.Model):
    name = models.CharField(max_length= 50)
    hackerrank_college_id = models.CharField(max_length=50, unique=True, default=None, null=True)
    students = models.ManyToManyField(User, related_name="colleges")

class Result(models.Model):
    user = models.ForeignKey('codingcenter.User', related_name="results", on_delete=models.CASCADE)
    question = models.ForeignKey('codingcenter.Question', related_name="results", on_delete=models.CASCADE)
    date_opened = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)