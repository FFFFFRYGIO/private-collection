from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books_list/", views.books_list, name="books_list"),
    path("add_books/", views.add_books, name="add_books"),
    path("edit_books/", views.edit_books, name="edit_books"),
]
