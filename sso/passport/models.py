from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.


class UserProfile(models.Model):
    id = models.AutoField(null=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128)
    mobile = models.CharField()
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

    objects = ''
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['name']

