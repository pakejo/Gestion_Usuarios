from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.views.generic.edit import FormView

from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm
from .functions import code_generator
from .models import User


# Create your views here.
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        code = code_generator()
        user = User.objects.create_user(
            username=form.cleaned_data['username'], email=form.cleaned_data['email'],
            password=form.cleaned_data['password1'], name=form.cleaned_data['name'],
            surname=form.cleaned_data['surname'], genre=form.cleaned_data['genre'],
            codlogin=code
        )
        topic = 'Email verification'
        message = 'Verification code: ' + code
        email = 'Put your email here'
        send_mail(topic, message, email, [form.cleaned_data['email']])
        return HttpResponseRedirect(
            reverse('users_app:user-verification', kwargs={'pk': user.id})
        )


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutUser(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )


class UpdatePassword(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('home_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        logged_user = self.request.user
        user = authenticate(
            username=logged_user.username,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            logged_user.set_password(new_password)
            logged_user.save()

        logout(self.request)
        return super(UpdatePassword, self).form_valid(form)


class CodeVerification(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerification, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs['pk']})
        return kwargs

    def form_valid(self, form):
        User.objects.filter(id=self.kwargs['pk']).update(is_active=True)
        return super(CodeVerification, self).form_valid(form)
