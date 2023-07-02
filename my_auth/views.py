from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProfileForm, UserProfileForm


# Create your views here.
def mylogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('books:index')
            else:
                error = True
                return render(request, 'my_auth/login.html', {'form': form, 'error': error})
        else:
            error = True
            return render(request, 'my_auth/login.html', {'form': form, 'error': error})
    error = False
    form = AuthenticationForm()
    return render(request, 'my_auth/login.html', {'form': form, 'error': error})

def mylogout(request):
    logout(request)
    return redirect('books:index')

@login_required(login_url='/admin/login/')
@staff_member_required
def create_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return render(request, 'my_auth/create_profile.html', {'user_form': user_form, 'profile_form': profile_form, 'success': True})
        else: 
           return render(request, 'my_auth/create_profile.html', {'user_form': user_form, 'profile_form': profile_form, 'error': True})
         
    else:
        user_form = UserProfileForm()
        profile_form = ProfileForm()
        return render(request, 'my_auth/create_profile.html', {'user_form': user_form, 'profile_form': profile_form,})
