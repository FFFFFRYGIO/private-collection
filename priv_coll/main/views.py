from django.shortcuts import render
from django.contrib import messages
from .models import Book
from .forms import AddBooks
from . import manage_books
# Create your views here.

add_keys = ['intitle', 'inauthor', 'inpublisher', 'subject', 'isbn', 'lccn', 'oclc']
attributes_keys = ['ISBN', 'Title', 'Authors', 'PublishedDate', 'PageCount', 'Thumbnail', 'Language']


def home(response):
    return render(response, 'main/home.html', {})


def books_list(response):
    if response.method == 'POST':
        # tutaj zrob poprawnie operacje edycji i usuwania
        # nalezy zmienic to jak to jest aktualnie robione
        # byc moze warto zapytać Marcela jak to powinno być
        pass
    else:
        return render(response, 'main/books_list.html', {'books_list': Book.objects.all(), 'attributes_keys': attributes_keys})


def add_books(response):
    if response.method == 'POST':
        form = AddBooks(response.POST)
        if form.is_valid():
            book_params = {}
            for i in add_keys:
                if form.cleaned_data[i]:
                    book_params[i] = form.cleaned_data[i]
            result = manage_books.add_books(book_params)
            if result.success:
                pass
                # messages.add_message('Adding succesful with ' + str(result.success) + ' successes')
            else:
                pass
                # messages.add_message('No books added')
            if result.errors:
                pass
                # messages.add_message('Errors with lack of ISBN number: ' + str(result.errors))
            if result.duplicates:
                pass
                # messages.add_message('Errors with duplicated books: ' + str(result.duplicates))
            return render(response, 'main/books_list.html', {})
    else:
        return render(response, 'main/add_books.html', {'form': AddBooks()})


def edit_book(response):
    return render(response, 'main/edit_book.html', {})
