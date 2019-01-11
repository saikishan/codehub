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

    description = models.CharField(default="Explain Yourself!", max_length=500)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'name', 'username']

    def __str__(self):
        return self.email

class Question(models.Model):
    title = models.CharField(max_length= 30)
    url = models.CharField(max_length= 100, unique= True)
    created_by = models.ForeignKey('codingcenter.User', related_name='created_questions', null=True, on_delete=models.SET_NULL)

class Assignment(models.Model):
    title = models.CharField(max_length=20)
    created_by = models.ForeignKey('codingcenter.User',related_name= 'created_assignments', null=True, on_delete=models.SET_NULL)
    questions = models.ManyToManyField(Question)
    participant = models.ManyToManyField(User)