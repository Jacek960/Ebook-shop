from django.urls import path
from .views import BookListView, BookDetailView, EbookCreateView, AuthorCreateView, EbookUpdate, EbookDelete, \
    HomePageView, GendreBooksView, SignUpView, PromoBooksView, AuthorBooksView, GendreCreateView, NewBooksView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('', HomePageView.as_view(), name='home_page'),
    path('books/<slug:slug>/', BookDetailView.as_view(), name='ebook_details'),
    path('add-book/', EbookCreateView.as_view(), name='add_ebook'),
    path('add-author/', AuthorCreateView.as_view(), name='add_author'),
    path('add-gendre/', GendreCreateView.as_view(), name='add_gendre'),
    path('book_edit/<pk>/',EbookUpdate.as_view(),name='edit-ebook'),
    path('book_delete/<pk>/',EbookDelete.as_view(),name='delete-ebook'),
    path('genrdre/<slug:gendre_slug>/', GendreBooksView.as_view(), name='ebook_gendre'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('promotion/', PromoBooksView.as_view(), name='promo_ebook'),
    path('new_books/', NewBooksView .as_view(), name='new_ebook'),
    path('author/<slug:autor_slug>/', AuthorBooksView.as_view(), name='ebook_author'),




]