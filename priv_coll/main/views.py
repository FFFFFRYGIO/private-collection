from django.shortcuts import render
from .forms import AddBooks
# Create your views here.


def home(response):
    return render(response, 'main/home.html', {})


def books_list(response):
    return render(response, 'main/books_list.html', {})


def add_books(response):
    return render(response, 'main/add_books.html', {'form': AddBooks()})


def edit_book(response):
    return render(response, 'main/edit_book.html', {})
