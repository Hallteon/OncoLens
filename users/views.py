from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from users.forms import LoginUserForm
from users.models import CustomUser
from utils.mixins import DataMixin


def logout_user(request):
    logout(request)

    return redirect('home')


class LoginUserView(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Вход')

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ShowUserAccountView(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Аккаунт {self.request.user.username}')

        return dict(list(context.items()) + list(c_def.items()))