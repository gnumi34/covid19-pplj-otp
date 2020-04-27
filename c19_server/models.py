from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'))
    mobile = models.CharField(_('mobile phone'), max_length=15, unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('owner')
        verbose_name_plural = _('owners')


class UserID(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userid', on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    nik = models.CharField(max_length=16)
    alamat = models.TextField()
    tanggal_lahir = models.CharField(max_length=8)

    class Meta:
        ordering = ['nama']


class Form(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    gejala_demam = models.BooleanField(default=False)
    usia = models.BooleanField(default=False)
    kontak = models.BooleanField(default=False)
    aktivitas = models.BooleanField(default=False)
    gejala_lain = models.TextField()
    kategori = models.PositiveSmallIntegerField(default=0)
    userid = models.ForeignKey(UserID, related_name='forms', on_delete=models.CASCADE)
