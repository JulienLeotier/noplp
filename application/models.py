"""
    models.py
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from .managers import CustomUserManager


class Categorie(models.Model):
    name = models.CharField(max_length=250, unique=True)
    points = models.IntegerField()
    use = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(Categorie, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Musique(models.Model):
    url = models.URLField(max_length=250,
                          db_index=True, unique=True, blank=True)
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    use = models.BooleanField(default=False)
    categorie = models.ForeignKey(
        Categorie, on_delete=models.CASCADE, to_field='name')

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.author = self.author.upper()
        return super(Musique, self).save(*args, **kwargs)

    def __str__(self):
        return "%s -- %s -- %s" % (self.name, self.author, self.categorie.name)


class Historique(models.Model):
    primary_user = models.ForeignKey(
        'CustomUser', related_name='related_primary_manual_roats', verbose_name="First Player", on_delete=models.CASCADE)
    secondary_user = models.ForeignKey('CustomUser', related_name='related_secondary_manual_roats',
                                       verbose_name="Second Player", blank=True, null=True, on_delete=models.CASCADE)

    scoreUser = models.IntegerField(default=0)
    scoreUser2 = models.IntegerField(default=0)
    categorie = models.ManyToManyField(Categorie, blank=True)

    def __str__(self):
        if self.scoreUser > self.scoreUser2:
            return "%s vs %s ---> %s win" % (self.primary_user.pseudo, self.secondary_user.pseudo, self.primary_user.pseudo)
        elif self.scoreUser == self.scoreUser2:
            return "%s vs %s ---> egalité" % (self.primary_user.pseudo, self.secondary_user.pseudo)
        else:
            return "%s vs %s ---> %s win" % (self.primary_user.pseudo, self.secondary_user.pseudo, self.secondary_user.pseudo)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
        User
    """
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    pseudo = models.CharField(max_length=250)
    avatar = models.ImageField(upload_to='static/images')
    use = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.pseudo = self.pseudo.upper()
        return super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


class Challenge(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class ChallengeGroups(models.Model):
    challenge = models.ForeignKey(Challenge, verbose_name=_(
        "challenge"), on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name=_(
        "group"), on_delete=models.CASCADE)
    photos = models.ImageField(upload_to='static/images')
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.group.name + ' ' + self.challenge.name


class Photobooth(models.Model):
    photos = models.ImageField(upload_to='static/images')

    def __str__(self):
        return 'super photo'
