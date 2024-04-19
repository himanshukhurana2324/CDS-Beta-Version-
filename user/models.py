from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class signup(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    bloodGroup = models.CharField(max_length=100) 
    gender = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True, max_length=100)
    state = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'age', 'bloodGroup', 'gender', 'state']

    objects = UserManager()




# class signup(models.Model):
#     username=models.CharField( max_length=100)
#     age=models.CharField(max_length=100)
#     bloodgroup=models.CharField(max_length=100)
#     sex=models.CharField(max_length=100)
#     phone=models.CharField(max_length=100)
#     email=models.EmailField(primary_key=True,max_length=100)
#     state=models.CharField(max_length=100)
#     password=models.CharField(max_length=100)
#     cpassword=models.CharField(max_length=100)