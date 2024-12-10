from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from ..academicApp.models import Section, Area
from django.contrib.auth.models import Group

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, group=None):
        if not email:
            raise ValueError("Los usuarios deben tener un email")
        
        # Normalizamos el email
        email = self.normalize_email(email).lower()

        user = self.model(
            email=email,
            group=group
        )

        user.set_password(password)  # Aquí se cifra la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("Los superusuarios deben tener un email")

        # Normalizamos el email
        email = self.normalize_email(email).lower()

        user = self.model(
            email=email,
            password=password,  # Aquí asignamos la contraseña en texto plano
            is_staff=True,
            is_superuser=True
        )

        user.save(using=self._db)  # Guardamos el usuario
        return user
 
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    first_name = models.CharField( max_length=150)
    last_name = models.CharField( max_length=150)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.email

class CustomGroup(models.Model):
    group_name = models.CharField(max_length=100)
    teacher_guide = models.ForeignKey(Profile, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.group_name

class GroupUser(models.Model):
    group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE)
    student = models.CharField(max_length=200)

    def __str__(self):
        return self.group.group_name 