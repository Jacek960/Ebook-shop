from django.urls import path
from .views import BookListView, BookDetailView, EbookCreateView, AuthorCreateView, EbookUpdate, EbookDelete, \
    HomePageView, GendreBooksView, SignUpView, PromoBooksList, AuthorBooksView, GendreCreateView, NewBooksList, \
    PublisherCreateView, SearchView
from books import views
urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('', HomePageView.as_view(), name='home_page'),
    path('books/<slug:slug>/', BookDetailView.as_view(), name='ebook_details'),
    path('add-book/', EbookCreateView.as_view(), name='add_ebook'),
    path('add-author/', AuthorCreateView.as_view(), name='add_author'),
    path('add-gendre/', GendreCreateView.as_view(), name='add_gendre'),
    path('add-publisher/', PublisherCreateView.as_view(), name='add_publisher'),
    path('book_edit/<pk>/',EbookUpdate.as_view(),name='edit-ebook'),
    path('book_delete/<pk>/',EbookDelete.as_view(),name='delete-ebook'),
    path('genre/<slug:gendre_slug>/', GendreBooksView.as_view(), name='ebook_gendre'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('promotion/', PromoBooksList.as_view(), name='promo_ebook'),
    path('new_books/', NewBooksList.as_view(), name='new_ebook'),
    path('author/<slug:autor_slug>/', AuthorBooksView.as_view(), name='ebook_author'),
    path('search/', SearchView.as_view(), name='search'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add_to_cart/<int:id_product>', views.AddItemToCardView.as_view(),name='add_book_to_cart'),
    path('remove_from_cart/<int:id_product>', views.RemoveItemFromCardView.as_view(),name='remove_book_from_cart'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('my_books/', views.MyEbooks.as_view(), name='my-books'),
    path('order_history/', views.OrderHistory.as_view(), name='order-history'),
    path('top-10/', views.BestRated.as_view(), name='top-10'),





]