from collections import namedtuple

from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Book
from .forms import AddBooks, AddNewBook, EditBook
from . import manage_books

# Create your views here.

add_keys = ["intitle", "inauthor", "inpublisher", "subject", "isbn", "lccn", "oclc"]
attributes_keys = ["ISBN", "Title", "Authors", "Published Date", "Page Count", "Thumbnail", "Language", "Cost"]


def home(response):
    """summarization of library, button to remove all books"""

    if not response.user.is_authenticated:
        return render(response, "main/home.html", {})
    if response.method == "POST":
        Book.objects.filter(user=response.user).delete()

    book_count = Book.objects.filter(user=response.user).count()
    book_cost = Book.objects.filter(user=response.user).aggregate(Sum("cost"))["cost__sum"]
    book_cost = book_cost if book_cost else 0.0
    book_without_cost = Book.objects.filter(user=response.user).exclude(cost__isnull=True).count()
    days_reading = int(book_count / ((1.75 + 4.1) / 2) * 30 + 0.5)
    months_reading = int(book_count / ((1.75 + 4.1) / 2) + 0.5)
    years_reading = int(book_count / ((1.75 + 4.1) / 2) / 12 + 0.5)
    reading_stats = namedtuple("stats", ["days", "months", "years"])(days_reading, months_reading, years_reading)

    return render(
        response,
        "main/home.html",
        {
            "book_count": book_count,
            "book_cost": book_cost,
            "book_without_cost": book_without_cost,
            "reading_stats": reading_stats,
        },
    )


def new_book(response):
    """form to add fully custom books"""

    if not response.user.is_authenticated:
        return redirect("home")
    messages = []
    if response.method == "POST":
        form = AddNewBook(response.POST)
        if form.is_valid():
            if Book.objects.filter(ISBN=form.cleaned_data["ISBN"], user=response.user):
                messages.append("Book with the ISBN " + form.cleaned_data["ISBN"] + " already exists!")
                return render(response, "main/new_book.html", {"messages": messages, "form": AddNewBook})
            else:
                b = Book()
                b.user = response.user
                b.ISBN = form.cleaned_data["ISBN"]
                b.title = form.cleaned_data["title"]
                b.authors = form.cleaned_data["authors"]
                b.publishedDate = form.cleaned_data["publishedDate"]
                b.pageCount = form.cleaned_data["pageCount"]
                b.thumbnail = form.cleaned_data["thumbnail"]
                b.language = form.cleaned_data["language"]
                b.cost = form.cleaned_data["cost"]
                b.save()
                messages.append("Book succesfully added!")
                return render(response, "main/new_book.html", {"form": AddNewBook, "messages": messages})
        else:
            messages.append("Input is not valid!")
    return render(response, "main/new_book.html", {"form": AddNewBook, "messages": messages})


def edit_book(response):
    """form to edit book chosen from list"""

    messages = []
    if not response.user.is_authenticated:
        return redirect("home")
    if response.method == "POST":
        form = EditBook(response.POST)
        if form.is_valid():
            result = manage_books.edit_book(9788301180638, response.user, form.cleaned_data)  # TODO: dynamic ISBN
            messages.append(result)
        else:
            messages.append("Form is not valid!")
        return redirect("books_list")
        return redirect("books_list", messages_parsed=messages)  # TODO: make it work
    else:
        b = Book.objects.get(ISBN="9788301180638", user=response.user)  # TODO: dynamic ISBN
        default_data = {
            "title": b.title,
            "authors": b.authors,
            "publishedDate": b.publishedDate,
            "pageCount": b.pageCount,
            "thumbnail": b.thumbnail,
            "language": b.language,
            "cost": b.cost,
        }
        return render(
            response, "main/edit_book.html", {"form": EditBook(default_data), "book_isbn": b.ISBN, "messages": messages}
        )


def books_list(response, messages_parsed=None):
    """all books user added, change to edit or delete them"""

    if not response.user.is_authenticated:
        return redirect("home")
    messages = []
    if messages_parsed:
        messages += messages_parsed
    if response.method == "POST" and response.POST.get("operation"):
        operation = response.POST.get("operation")[0]
        book_isbn = response.POST.get("operation")[1:]
        if operation == "E":  # Edit
            book = Book.objects.get(ISBN=book_isbn, user=response.user)
            return redirect("edit_book")
            return redirect("edit_book", isbn=book.ISBN)  # TODO: make it work
        elif operation == "D":  # Delete
            Book.objects.filter(ISBN=book_isbn, user=response.user).delete()
            messages.append("Book successfully deleted!")
    books = Book.objects.filter(user=response.user).order_by("ISBN")
    return render(
        response,
        "main/books_list.html",
        {"books_list": books, "attributes_keys": attributes_keys, "messages": messages},
    )


def add_books(response):
    """add book by keywords from api or from a file"""

    if not response.user.is_authenticated:
        return redirect("home")
    messages = []
    if response.method == "POST":
        if response.POST.get("submit") == "by_keys":
            form = AddBooks(response.POST)
            if form.is_valid():
                book_params = {}
                for i in add_keys:
                    if form.cleaned_data[i]:
                        book_params[i] = form.cleaned_data[i]
                result = manage_books.add_books(book_params=book_params, user=response.user)
                messages.append("Adding succesful with " + str(result.success) + " successes") if result.success else 0
                messages.append("No books added") if result.success == 0 else 0
                messages.append("Errors with lack of ISBN number: " + str(result.errors)) if result.errors else 0
                messages.append("Errors with duplicated books: " + str(result.duplicates)) if result.duplicates else 0
                return redirect("books_list")
                return redirect("books_list", messages_parsed=messages)  # TODO: make it work
            else:
                messages.append("Input is not valid!")
        elif response.POST.get("submit") == "by_file":
            result = manage_books.import_books_from_file(user=response.user)
            messages.append(result)
            return redirect("books_list")
            return redirect("books_list", messages_parsed=messages)  # TODO: make it work
    return render(response, "main/add_books.html", {"form": AddBooks(), "messages": messages})
