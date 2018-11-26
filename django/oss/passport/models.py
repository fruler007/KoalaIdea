from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import mail
# Create your models here.


class NewUserManger(BaseUserManager):
    user_in_migrations = True

    def _create_user(self, name, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not name:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        name = self.model.normalize_username(name)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=16)
    date_of_birth = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this'
                    ' admin site'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.')
    )
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = NewUserManger()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['name']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        mail.send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.name

    def get_short_name(self):
        return self.name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = ()
