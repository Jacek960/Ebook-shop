from django.urls import path
from .views import BookListView, BookDetailView, EbookCreateView, AuthorCreateView, EbookUpdate, EbookDelete

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/<slug:slug>/', BookDetailView.as_view(), name='ebook_details'),
    path('add-book/', EbookCreateView.as_view(), name='add_ebook'),
    path('add-author/', AuthorCreateView.as_view(), name='add_author'),
    path('book_edit/<pk>/',EbookUpdate.as_view(),name='edit-ebook'),
    path('book_delete/<pk>/',EbookDelete.as_view(),name='delete-ebook'),



]