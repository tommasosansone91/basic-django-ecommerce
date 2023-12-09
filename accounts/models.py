from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):  # only required fileds are put as input here
        
        if not email:
            raise ValueError("Users must have an email address")  # indicatd y the docs
        if not password:
            raise ValueError("Users must have a password")  # indicatd y the docs
        if not full_name:
            raise ValueError("Users must have a full name") 
        
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name
        )

        user_obj.set_password(password)  # setter per passwod
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)

        return user_obj
    
    # metodi per definire tpi di utente "predefiniti", con attributi uguale ad un valore prefissato
    
    def create_staffuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password = password,
            is_staff = True
        )
        return user
    
    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password = password,
            is_staff = True,
            is_admin = True
        )
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)  # is h* allowed to login?
    staff = models.BooleanField(default=False) # staff user, not superuser
    admin = models.BooleanField(default=False) # superuser
    timestamp = models.DateTimeField(auto_now_add=True) # superuser

    USERNAME_FIELD = 'email'

    # email and password are required

    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # extend extra data


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
        