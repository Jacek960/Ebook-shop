from django.urls import path
from .views import BookListView , BookDetailView





urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<slug:slug>/', BookDetailView.as_view(), name='ebook_details'),



]