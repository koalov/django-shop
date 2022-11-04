from allauth.account.models import EmailAddress
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',
                                verbose_name=_("User"))
    Genders = (
        (_('М'), _('Male')),
        (_('F'), _('Female')),
    )
    first_name = models.CharField(max_length=128, blank=True,
                                  verbose_name=_("First name"))
    last_name = models.CharField(max_length=128, blank=True,
                                 verbose_name=_("Last name"))
    org = models.CharField(max_length=128, blank=True,
                           verbose_name=_("Organization"))
    telephone = models.CharField(max_length=50, blank=True,
                                 verbose_name=_("Telephone"))
    birthday = models.DateField(null=True, verbose_name=_('BirthDay'))
    mod_date = models.DateTimeField(auto_now=True, error_messages={_('required'): ''},
                                    verbose_name=_('Last modified'))
    sex = models.CharField(max_length=1, choices=Genders, default='M',
                           verbose_name=_("Gender"))
    photo = models.ImageField(upload_to="users_avatar/", verbose_name=_("User image"))

    class Meta:
        verbose_name = _('User Profile')

    def __str__(self):
        return "{}'s profile".format(self.user.__str__())

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def photo_img(self):
        if self.photo:
            from django.utils.safestring import mark_safe
            return mark_safe(
                u'<a href="{0}" target="_blank"><img src="{0}" width="100"/></a>'.format(
                    self.photo.url))
        else:
            return _('No image')

    photo_img.short_description = _('Image')
    photo_img.allow_tags = True

    image_in_profile = ImageSpecField(source='photo',
                                      processors=[ResizeToFill(400, 400)],
                                      format='JPEG',
                                      options={'quality': 60})