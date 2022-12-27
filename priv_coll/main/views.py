from django.shortcuts import render, redirect
from .models import Book
from .forms import AddBooks, AddNewBook
from . import manage_books
# Create your views here.

add_keys = ['intitle', 'inauthor', 'inpublisher', 'subject', 'isbn', 'lccn', 'oclc']
attributes_keys = ['ISBN', 'Title', 'Authors', 'PublishedDate', 'PageCount', 'Thumbnail', 'Language']


def home(response):
    return render(response, 'main/home.html', {})


def new_book(response):
    messages = []
    if response.method == "POST":
        form = AddNewBook(response.POST)
        if form.is_valid():
            if Book.objects.filter(ISBN=form.cleaned_data["ISBN"]):
                messages.append("Book with the ISBN " + form.cleaned_data["ISBN"] + " already exists!")
                return render(response, 'main/new_book.html', {'messages': messages, 'form': AddNewBook})
            else:
                b = Book()
                b.ISBN = form.cleaned_data["ISBN"]
                b.authors = form.cleaned_data["authors"]
                b.publishedDate = form.cleaned_data["publishedDate"]
                b.pageCount = form.cleaned_data["pageCount"]
                b.thumbnail = form.cleaned_data["thumbnail"]
                b.language = form.cleaned_data["language"]
                # response.user.book.add(b)
                b.save()
                messages.append("Book succesfully added!")
                # return redirect('books_list', messages_parsed=messages)
                return render(response, 'main/new_book.html', {'form': AddNewBook, 'messages': messages})
        else:
            messages.append('Input is not valid!')
    return render(response, 'main/new_book.html', {'form': AddNewBook, 'messages': messages})


def books_list(response, messages_parsed=None):
    messages = []
    if messages_parsed:
        messages += messages_parsed
    if response.method == 'POST' and response.POST.get("operation"):
        operation = response.POST.get("operation")[0]
        book_isbn = response.POST.get("operation")[1:]
        if operation == 'E':  # Edit
            book = Book.objects.get(ISBN=book_isbn)
            return render(response, 'main/edit_book.html', {'book': book})
        elif operation == 'D':  # Delete
            Book.objects.filter(ISBN=book_isbn).delete()
            messages.append("Book successfully deleted!")
    books = Book.objects.all()
    return render(response, 'main/books_list.html', {
        'books_list': books, 'attributes_keys': attributes_keys, 'messages': messages})


def add_books(response):
    messages = []
    if response.method == 'POST':
        form = AddBooks(response.POST)
        if form.is_valid():
            book_params = {}
            for i in add_keys:
                if form.cleaned_data[i]:
                    book_params[i] = form.cleaned_data[i]
            result = manage_books.add_books(book_params)
            messages.append('Adding succesful with ' + str(result.success) + ' successes') if result.success else 0
            messages.append('No books added') if result.success == 0 else 0
            messages.append('Errors with lack of ISBN number: ' + str(result.errors)) if result.errors else 0
            messages.append('Errors with duplicated books: ' + str(result.duplicates)) if result.duplicates else 0
            return redirect('books_list', messages_parsed=messages)
        else:
            messages.append('Input is not valid!')
    return render(response, 'main/add_books.html', {'form': AddBooks(), 'messages': messages})


def edit_book(response):
    return render(response, 'main/edit_book.html', {})
