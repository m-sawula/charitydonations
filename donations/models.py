from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


# ------------authorization------------------

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Replaces User Model, sets e-mail as unique login.
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# ----------app models------------------

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'kategoria'
        verbose_name_plural = 'kategorie'


class Institution(models.Model):
    INST_TYPE = (
        (1, 'fundacja'),
        (2, 'organizacja pozarządowa'),
        (3, 'zbiórka lokalna'),
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, blank=False)
    type = models.IntegerField(choices=INST_TYPE, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'instytucja'
        verbose_name_plural = 'instytucje'


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name='liczba worków')
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='institutions')
    adress = models.CharField(max_length=64, verbose_name='ulica, nr domu, nr lokalu')
    phone_number = models.IntegerField(verbose_name='numer telefonu')
    city = models.CharField(max_length=64, verbose_name='miasto')
    zip_code = models.IntegerField(verbose_name='kod pocztwy xx-xxx')
    pick_up_date = models.DateField(null=True, verbose_name='data odbioru')
    pick_up_time = models.TimeField(null=True, verbose_name='godzina odbioru')
    pick_up_comment = models.TextField(verbose_name='uwagi dla kuriera')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None)
