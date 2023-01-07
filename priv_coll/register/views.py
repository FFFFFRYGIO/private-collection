from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def register(response):
    """parse and handle registration form"""
    messages = []
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            render(response, "register/register.html", {"form": form, "messages": messages})
    else:
        form = UserCreationForm()

    return render(response, "register/register.html", {"form": form, "messages": messages})
