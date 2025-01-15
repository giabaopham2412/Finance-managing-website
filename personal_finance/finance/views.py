from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .forms import IncomeForm, ExpenseForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
import calendar
from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.timezone import now
# Create your views here.
def home(request):
    return render(request, 'finance/home.html')
@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('financial_report')  # Chuyển hướng đến trang báo cáo tài chính
    else:
        form = IncomeForm(initial={'date': now().date()})  # Tự động điền ngày hiện tại
    return render(request, 'finance/add_income.html', {'form': form})
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('financial_report')  # Sau khi lưu, chuyển hướng đến trang báo cáo tài chính
    else:
        form = ExpenseForm()
    return render(request, 'finance/add_expense.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Sau khi đăng nhập thành công, chuyển hướng về trang home
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})