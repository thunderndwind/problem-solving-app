from django.shortcuts import render, redirect
from .forms import SimpleUserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'problem_solving/home.html')



def register(request):
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = SimpleUserCreationForm()

    return render(request, 'problem_solving/register.html', {'form': form})

class CustomLoginView(auth_views.LoginView):
    template_name = 'problem_solving/login.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(*args, **kwargs)

@login_required
def dashboard(request):
    return render(request, 'problem_solving/dashboard.html')

def custom_logout(request):
    logout(request)
    return redirect('home')