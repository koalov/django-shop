from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView

# Create your views here.


class ProfileView(LoginRequiredMixin, DetailView):
    context_object_name = "current_user"
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    # def account_profile(self, request):
    #     return render(self.request, 'profile.html')
