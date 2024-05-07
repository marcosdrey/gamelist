from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.messages import add_message, constants
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            add_message(request, constants.WARNING, "You're already logged in!")
            return redirect('home')
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        agree_terms = request.POST.get('agree_terms')
        profile_photo = request.FILES.get('profile_photo')
        users = User.objects.filter(username=username)
        if password != confirm_password:
            add_message(request, constants.WARNING, 'The passwords are different!')
            return redirect('register')
        if len(password) < 6:
            add_message(request, constants.WARNING, 'Password must have, at least, 6 characters!')
            return redirect('register')
        if not agree_terms:
            add_message(request, constants.WARNING, 'You must agree to the terms and conditions!')
            return redirect('register')
        if users.exists():
            add_message(request, constants.WARNING, 'That username already exists!')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
        )
        if profile_photo:
            profile = Profile(user=user, profile_photo=profile_photo)
        else:
            profile = Profile(user=user)
        profile.save()
        
        add_message(request, constants.SUCCESS, 'Account was created successfully!')
        return redirect('login')
        

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            add_message(request, constants.WARNING, "You're already logged in!")
            return redirect('home')
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('home')
        add_message(request, constants.ERROR, 'Wrong credentials. Try again!')
        return redirect('login')
    

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return render(request, 'logout.html')
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'GET':
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'profile-page.html', context)
    elif request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            add_message(request, constants.SUCCESS, 'Changes made successfully!')
        else:
            add_message(request, constants.ERROR, 'Credentials were invalid. Try again.')
        return redirect('profile-page')
        