from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(response):
    return HttpResponse("<h1>tech with tim!</h>")


def books_list(response):
    return HttpResponse("<h1>books_list</h>")


def add_books(response):
    return HttpResponse("<h1>add_books</h>")


def edit_books(response):
    return HttpResponse("<h1>edit_books</h>")
