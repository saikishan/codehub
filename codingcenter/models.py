from django.db import models
from django.db.models import Count,F
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
    last_scraped = models.DateTimeField(auto_now_add=True)

    def has_user(self,user):
        return True if Question.objects.filter(id=self.id, solved_by__in = [user]).count() == 1 else False

    def get_dashboard(self,to_list=False):
        "add the sample data and test the set"
        data = Question.objects.filter(id=self.id).values(username = F("results__user__username"),status = F("results__status"))
        return data


class Assignment(models.Model):
    title = models.CharField(max_length=20)
    created_by = models.ForeignKey('codingcenter.User',related_name= 'created_assignments', null=True, on_delete=models.SET_NULL)
    questions = models.ManyToManyField(Question)
    participants = models.ManyToManyField('codingcenter.User', related_name='assignments')

    def has_user(self, user):
        return True if (Assignment.objects.filter(id=self.id, participants_id = user.id).count() == 1) else False

    def get_dashboard(self, question_id=None):
        '''
        add the filter the support with and with out question id
        this should also return total based
        type of query.
        '''
        if not question_id:
            return Assignment.objects.filter(id=self.id, questions__results__status=True,
                                      questions__results__question__in=F('questions'),
                                      questions__results__user__in=F('participants')).values(
                username = F('questions__results__user__username')).annotate(total=Count('questions__results')).order_by('total').reverse()
        else:
            return Assignment.objects.filter(id=self.id, questions__results__question=question_id, questions__results__user__in=F('participants')).values(username = F("questions__results__user__username"),status = F("questions__results__status"))


class College(models.Model):
    name = models.CharField(max_length= 50)
    hackerrank_college_id = models.CharField(max_length=50, unique=True, default=None, null=True)
    students = models.ManyToManyField(User, related_name="colleges")

class Result(models.Model):
    user = models.ForeignKey('codingcenter.User', related_name="results", on_delete=models.CASCADE)
    question = models.ForeignKey('codingcenter.Question', related_name="results", on_delete=models.CASCADE)
    date_opened = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)