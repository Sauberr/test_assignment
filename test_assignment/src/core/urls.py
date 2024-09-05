from django.urls import path

from core.views import IndexView, BookList

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("books/", BookList.as_view(),  name="books_list"),
]
