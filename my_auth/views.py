from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import PasswordChangeView
from django.views import generic
from .forms import ProfileForm, UserProfileForm, CustomPasswordChangeForm, CustomAuthenticationForm
from books.models import Borrowing


# Create your views here.
def mylogin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('my-auth:my-account')
            else:
                error = True
                return render(request, 'my_auth/login.html', {'form': form, 'error': error})
        else:
            error = True
            return render(request, 'my_auth/login.html', {'form': form, 'error': error})
    error = False
    form = CustomAuthenticationForm()
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

@login_required(login_url='/web-auth/login')
def my_account(request):
    borrowings = Borrowing.objects.filter(borrower=request.user.profile).prefetch_related()
    return render(request, 'my_auth/my_account.html', {'borrowings': borrowings})

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'my_auth/change_password.html'
    success_url = '/web_auth/my-account/change-password/'

class PorfilePhotoChangeView(generic.UpdateView):
    form_class = ProfileForm
    template_name = 'my_auth/change_photo.html'
    success_url = '/web_auth/my-account/change-photo/'

    def get_object(self, queryset=None):
        queryset = self.request.user.profile
        return queryset
    
    def form_valid(self, form):
        response = super().form_valid(form)
        photo_clear = self.request.POST.get('photo-clear', False)
        
        if photo_clear:
            self.object.photo.delete()
            self.object.photo = None
            self.object.save()

        if 'photo' in self.request.FILES:
            self.object.photo = self.request.FILES['photo']
            self.object.save()

        return response
        