from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import add_message, constants
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView, LoginView
from .forms import UserUpdateForm, ProfileUpdateForm, PersonalizedUserCreationForm


class RegisterPageView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = PersonalizedUserCreationForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        add_message(self.request, constants.SUCCESS, 'Account was created successfully!')
        return super().get_success_url()


class LoginPageView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True


class LogoutPageView(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'


class ProfilePageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.__get_context(request)
        return render(request, 'profile-page.html', context)

    def post(self, request, *args, **kwargs):
        context = self.__get_context(request)

        if context['u_form'].is_valid() and context['p_form'].is_valid():
            context['u_form'].save()
            context['p_form'].save()
            add_message(request, constants.SUCCESS, 'Changes made successfully!')
            request.session.pop('original_infos', None)
            return redirect('profile-page')
        else:
            context['original_infos'] = request.session.get('original_infos')
            return render(request, 'profile-page.html', context)

    def __get_context(self, request):
        if request.method == 'GET':
            user_form = UserUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=request.user.profile)
            request.session['original_infos'] = {
                'username': request.user.username,
                'email': request.user.email,
                'profile_photo': request.user.profile.profile_photo.url
            }
        elif request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES,
                                             instance=request.user.profile)

        context = {
            'u_form': user_form,
            'p_form': profile_form,
            'original_infos': request.session.get('original_infos')
        }
        return context
