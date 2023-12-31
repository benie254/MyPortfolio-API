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
class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
            """
            Create and save a user with the given username, email, and password.
            """
            if not username:
                raise ValueError("The given username must be set")

            if username is None:
                raise TypeError('Users must have a username.')

            if email is None:
                raise TypeError('Users must have an email address.')

            email = self.normalize_email(email)
            # Lookup the real model class from the global app registry so this
            # manager method can be used in migrations. This is fine because
            # managers are by definition working on the real model.
            GlobalUserModel = apps.get_model(
                self.model._meta.app_label, self.model._meta.object_name
            )
            username = GlobalUserModel.normalize_username(username)
            user = self.model(username=username, email=email, **extra_fields)
            user.password = make_password(password)
            user.save(using=self._db)
            return user
    
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if password is None:
            raise TypeError('Admins must have a password.')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
    
    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth.get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()
    
    # A few helper functions for common logic between User and AnonymousUser.
    def _user_get_permissions(user, obj, from_name):
        permissions = set()
        name = "get_%s_permissions" % from_name
        for backend in auth.get_backends():
            if hasattr(backend, name):
                permissions.update(getattr(backend, name)(user, obj))
        return permissions


    def _user_has_perm(user, perm, obj):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, "has_perm"):
                continue
            try:
                if backend.has_perm(user, perm, obj):
                    return True
            except PermissionDenied:
                return False
        return False
    
    def _user_has_module_perms(user, app_label):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, "has_module_perms"):
                continue
            try:
                if backend.has_module_perms(user, app_label):
                    return True
            except PermissionDenied:
                return False
        return False
    
class MyUser(AbstractBaseUser,PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    
    username = models.CharField(
        _("username"),
        max_length=60,
        unique=True,
        help_text=_(
            "Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with this username already exists."),
        }
    )
    email = models.EmailField(
        _("email address"),unique=True,
        error_messages={
            "unique": _("A user with this email already exists."),
        }
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = MyAccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email',]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Password(models.Model):
    username = models.CharField(max_length=120,null=True,blank=True)
    email = models.EmailField(max_length=120,null=True,blank=True)

class Project(models.Model):
    name = models.CharField(max_length=500,default='')
    first_created = models.DateField(default=timezone.now)
    summary = models.TextField(max_length=1000,default='')
    long_description = models.TextField(max_length=10000,default='')
    featured_img = models.URLField(max_length=5000,default='')
    screenshot = models.URLField(max_length=5000,default='',null=True,blank=True)
    screenshot_2 = models.URLField(max_length=5000,default='',null=True,blank=True)
    live_link = models.URLField(max_length=1000,default='')
    git_link = models.URLField(max_length=1000,default='')
    documentation = models.URLField(max_length=1000,default='')
    TECHS = (
        ('Django, Angular, SQL, DRF, Firebase, Railway','Django, Angular, SQL, DRF, Firebase, Railway'),
        ('Django, Angular, SQL, DRF, Firebase, Vercel','Django, Angular, SQL, DRF, Firebase, Vercel'),
        ('Django, SQL, DRF, Railway','Django, SQL, DRF, Railway'),
        ('Django, SQL, DRF, Vercel','Django, SQL, DRF, Vercel'),
        )
    technologies = models.CharField(choices=TECHS,max_length=1000,default='')
    FEATS = (
        ('Authentication, Admin, Email Service, Notifier, Search Filter, Lazy Loading, Error Handling, Form Validation','Authentication, Admin, Email Service, Notifier, Search Filter, Lazy Loading, Error Handling, Form Validation'),
        ('Admin, Email Service, Notifier, Search Filter, Lazy Loading, Error Handling, Form Validation','Admin, Email Service, Notifier, Search Filter, Lazy Loading, Error Handling, Form Validation'),
        ('Authentication, Email Service, SMS Service, Notifier, Error Handling, Form Validation','Authentication, Email Service, SMS Service, Notifier, Error Handling, Form Validation'),
        ('Authentication, Email Service, Notifier, Error Handling, Form Validation','Authentication, Email Service, Notifier, Error Handling, Form Validation'),
        ('Email Service, Notifier, Search Filter, Error Handling, Form Validation','Email Service, Notifier, Search Filter, Error Handling, Form Validation'),
        ('Email Service, Notifier, Error Handling, Form Validation','Email Service, Notifier, Error Handling, Form Validation'),
        ('Custom Authentication, API, Email Service','Custom Authentication, API, Email Service'),
        ('Custom Authentication, API, Email Service, SMS Service', 'Custom Authentication, API, Email Service, SMS Service'),
        ('API, Email Service, SMS Service', 'API, Email Service, SMS Service'),
        ('API, Email Service', 'API, Email Service'),
        ('API', 'API'),
        )
    features = models.CharField(choices=FEATS,max_length=5000,default='')
    FEATURE = (('featured','featured'),('not featured','not featured'))
    featured = models.CharField(choices=FEATURE,max_length=500,default='')
    PINS = (('pinned','pinned'),('unpinned','unpinned'))
    pinned = models.CharField(choices=PINS,max_length=500,null=True,blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Like(models.Model):
    LIKES = (('like','like'),('dislike','dislike'))
    like = models.CharField(choices=LIKES,max_length=60,null=True,blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.like
    
class Comment(models.Model):
    comment = models.TextField(max_length=5000,null=True,blank=True)
    commented_by = models.CharField(max_length=200,null=True,blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
    
class Contact(models.Model):
    name = models.CharField(max_length=300,null=True,blank=True)
    email = models.EmailField(max_length=500,null=True,blank=True)
    message = models.TextField(max_length=10000,null=True,blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    