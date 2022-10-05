from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from users.forms import ProfileForm
from users.models import UserProfile


@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def profile_update(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.birthday = form.cleaned_data['birthday']
            user_profile.sex = form.cleaned_data['sex']
            user_profile.photo = form.cleaned_data['photo']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:profile'))
    else:
        default_data = {'first_name': user.first_name,
                        'last_name': user.last_name,
                        'org': user_profile.org,
                        'telephone': user_profile.telephone,
                        'sex': user_profile.sex,
                        'photo': user_profile.photo,
                        'birthday': user_profile.birthday,
                        }
        form = ProfileForm(default_data)

    return render(request, 'profile_update.html', {'form': form, 'user': user})