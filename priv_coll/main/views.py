from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(response):
    return render(response, 'main/home.html', {})


def books_list(response):
    return render(response, 'main/books_list.html', {})


def add_books(response):
    return render(response, 'main/add_books.html', {})


def edit_book(response):
    return render(response, 'main/edit_book.html', {})
