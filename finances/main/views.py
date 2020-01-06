from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def homepage(request):
    return render(
        request=request,
        template_name="main/home.html",
    )


def register(request):
    if request.method == "POST":
        return post_register(request)

    form = UserCreationForm()
    return render(
        request=request,
        template_name="main/register.html",
        context={"form": form}
    )


def post_register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')
        messages.success(request, f"New account created {username}")
        login(request, user)
        return redirect("main:homepage")
    else:
        for m in form.error_messages:
            messages.error(request, f"{m}:{form.error_messages[m]}")

    return render(
        request=request,
        template_name="main/register.html",
        context={"form": form}
    )


def login_request(request):
    if request.method == "POST":
        return post_register(request)

    form = AuthenticationForm()
    return render(
        request=request,
        template_name="main/login.html",
        context={"form": form}
    )


def post_login(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {username}")
            return redirect("main:homepage")
        else:
            messages.error(request, "authentication failed")
    else:
        for m in form.error_messages:
            messages.error(request, f"{m}:{form.error_messages[m]}")
    return render(
        request=request,
        template_name="main/login.html",
        context={"form": form}
    )


def logout_request(request):
    logout(request)
    messages.success(request, f"You've been logged out")
    return redirect("main:homepage")
