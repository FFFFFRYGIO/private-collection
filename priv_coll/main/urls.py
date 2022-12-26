from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books_list/", views.books_list, name="books_list"),
    path("add_books/", views.add_books, name="add_books"),
    path("edit_book/", views.edit_book, name="edit_books"),
]
