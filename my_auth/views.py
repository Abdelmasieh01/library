from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

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