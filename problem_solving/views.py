from django.shortcuts import render, get_object_or_404, redirect
from .forms import SimpleUserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Problem, Solution
from .forms import SolutionForm
import json
import subprocess

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

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'problem_solving/problem_list.html', {'problems': problems})

@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.user = request.user
            solution.problem = problem
            solution.passed = evaluate_solution(problem, solution.code)
            solution.save()
            return redirect('solution_result', pk=solution.pk)
    else:
        form = SolutionForm()

    return render(request, 'problem_solving/problem_details.html', {'problem': problem, 'form': form})

def solution_result(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    if not solution.passed: 
        solution.passed = evaluate_solution(solution.problem, solution.code)
        solution.save()
    return render(request, 'problem_solving/solution_result.html', {'solution': solution})

def evaluate_solution(problem, code):
    test_cases = problem.test_cases

    inputs = test_cases.get('inputs', [])
    outputs = test_cases.get('outputs', [])

    if len(inputs) != len(outputs):
        print("Error: Number of inputs and outputs do not match.")
        return False

    for i, input_data in enumerate(inputs):
        expected_output = outputs[i]

        input_str = ' '.join(map(str, input_data))

        try:
            process = subprocess.run(
                ['python3', '-c', code], 
                input=input_str.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )

            result_output = process.stdout.decode().strip()
            if result_output != str(expected_output):
                return False
        except Exception as e:
            print(f"Exception occurred: {e}")
            return False
    return True