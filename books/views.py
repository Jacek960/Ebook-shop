import random
from unicodedata import decimal

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View

from books.forms import EbookForm, AuthorForm, SignUpForm, GendreForm, PublisherForm
from books.models import Ebook, Gendre, Autor, Banner, MainBanner, Cart, CartProduct
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'books/signup.html'


class BookListView(ListView):
    paginate_by = 5
    template_name='books/book_list.html'
    model = Ebook

class BookDetailView(DetailView):
    template_name = 'books/book_details.html'
    model = Ebook
    pk_url_kwarg = 'ebook_slug'


class HomePageView(View):
    def get(self,request,):
        ebooks=Ebook.objects.all()
        gendres = Gendre.objects.all().order_by('name')
        gendre_count = Gendre.objects.annotate(total_gendre=Count('ebook')).order_by('name')
        last5_ebooks = Ebook.objects.order_by('-created')[0:5]
        discount_books_list = list(Ebook.objects.filter(discount_percent__gt=0))
        random.shuffle(discount_books_list)
        discount_books = discount_books_list[0:5]
        banners=Banner.objects.filter(is_active=True)
        mainbaner=MainBanner.objects.all()

        return render(request,'books/home.html',{'gendres':gendres,
                                                 'gendre_count':gendre_count,
                                                 'ebooks':ebooks,
                                                 'last5_ebooks':last5_ebooks,
                                                 'discount_books':discount_books,
                                                 'banners':banners,
                                                 'mainbaner':mainbaner,
                                                 })

class GendreBooksView(View):
    def get(self,request,gendre_slug=None):
        gendre_books = Ebook.objects.all()
        if gendre_slug:
            gendre= Gendre.objects.get(slug=gendre_slug)
            gendre_books=gendre_books.filter(gendre=gendre)
        return render(request,'books/gendre_list.html',{'gendre_books':gendre_books,'gendre':gendre})



class EbookCreateView(PermissionRequiredMixin,CreateView):
    form_class = EbookForm
    template_name = 'books/add_book_form.html'
    success_url = '/books/'
    permission_required = 'books.add_ebook'

class AuthorCreateView(PermissionRequiredMixin,CreateView):
    form_class = AuthorForm
    template_name = 'books/add_author_form.html'
    success_url = '/books/'
    permission_required = 'books.add_autor'

class GendreCreateView(PermissionRequiredMixin,CreateView):
    form_class = GendreForm
    template_name = 'books/add_gendre_form.html'
    success_url = '/books/'
    permission_required = 'books.add_gendre'

class PublisherCreateView(PermissionRequiredMixin,CreateView):
    form_class = PublisherForm
    template_name = 'books/add_publisher_form.html'
    success_url = '/books/'
    permission_required = 'books.add_publisher'

class EbookUpdate(PermissionRequiredMixin,UpdateView):
    model = Ebook
    form_class = EbookForm
    template_name = 'books/add_book_form.html'
    success_url = '/books/'
    permission_required = 'books.change_ebook'

class EbookDelete(PermissionRequiredMixin,DeleteView):
    model = Ebook
    template_name = 'books/ebook_delete.html'
    success_url = '/books/'
    permission_required = 'books.delete_ebook'

class PromoBooksView(View):
    def get(self,request):
        promo_books=Ebook.objects.filter(discount_percent__gt=0)
        return render(request,'books/promo_books.html',{'promo_books':promo_books})

class AuthorBooksView(View):
    def get(self,request,autor_slug=None):
        autor_books = Ebook.objects.all()
        if autor_slug:
            autor = Autor.objects.get(slug=autor_slug)
            autor_books=autor_books.filter(autor=autor)
        return render(request, 'books/author_list.html', {'autor_books': autor_books,'autor':autor})

class NewBooksView(View):
    def get(self,request):
        new_books=Ebook.objects.order_by('-created')
        return render(request,'books/new_books.html',{'new_books':new_books})


class SearchView(View):
    def get(self,request):
        books = None
        query = None
        if 'q' in request.GET:
            query = request.GET.get('q')
            books = Ebook.objects.all().filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(autor__name__icontains=query))
        return render(request, 'books/search.html', {'query': query, 'books': books})


class AddItemToCardView(LoginRequiredMixin,View):

    def get(self, request, id_product):
        cart, created= Cart.objects.get_or_create(user=request.user)
        ebook = Ebook.objects.get(id=id_product)
        cart.product.add(ebook)
        return redirect('cart')


class RemoveItemFromCardView(LoginRequiredMixin,View):

    def get(self, request, id_product):
        cart = Cart.objects.get(user=request.user)
        ebook = Ebook.objects.get(id=id_product)
        cart.product.remove(ebook)
        return redirect('cart')



class CartView(LoginRequiredMixin,View):

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        total = 0
        for item in cart.product.all():
            if  item.discount_percent== 0:
                total += item.price_brutto()
            elif item.discount_percent > 0:
                total += item.price_brutto_discount()
        return render(request, 'books/shopping_cart.html', {'cart':cart,'total':total})


