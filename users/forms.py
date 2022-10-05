from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            "first_name",
            "last_name",
            "org",
            "telephone",
            "photo",
            'sex',
            'birthday',

        )
        widgets = {
            "birthday": forms.DateInput(attrs={'type': 'date'}),
        }




class SignupForm(forms.Form):

    def signup(self, request, user):
        user_profile = UserProfile()
        user_profile.user = user
        user.save()
        user_profile.save()