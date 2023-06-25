from django.db import models
from django.utils import timezone 
import datetime as dt 
from django.http import Http404
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.hashers import make_password 
from django.apps import apps 
from django.contrib import auth 
from django.core.exceptions import PermissionDenied 
from django.core.mail import send_mail 
from django.contrib.auth.validators import UnicodeUsernameValidator 
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
