from django.urls import path, include
from register.views import register
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("books_list/", views.books_list, name="books_list"),
    path("add_books/", views.add_books, name="add_books"),
    path("edit_book/", views.edit_book, name="edit_book"),
    path("new_book/", views.new_book, name="new_book"),
    path("register/", register, name="register"),
    path("", include("django.contrib.auth.urls")),
]
