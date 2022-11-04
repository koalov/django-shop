from allauth.account.models import EmailAddress
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    Genders = (
        ('М', 'Мужчина'),
        ('Ж', 'Женщина'),
    )
    first_name = models.CharField('First_Name', max_length=128, blank=True)
    last_name = models.CharField('Last_Name', max_length=128, blank=True)
    org = models.CharField('Organization', max_length=128, blank=True)
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    birthday = models.DateField('BirthDay', null=True)
    mod_date = models.DateTimeField('Last modified', auto_now=True, error_messages={'required': ''})
    sex = models.CharField('Пол', max_length=1, choices=Genders, default='M')
    photo = models.ImageField(upload_to="users_avatar/", verbose_name="Аватар")

    class Meta:
        verbose_name = 'User Profile'

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
            return '(Нет изображения)'

    photo_img.short_description = 'Картинка'
    photo_img.allow_tags = True

    image_in_profile = ImageSpecField(source='photo',
                                      processors=[ResizeToFill(400, 400)],
                                      format='JPEG',
                                      options={'quality': 60})