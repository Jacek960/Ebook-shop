import random
from unicodedata import decimal

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View

from books.forms import EbookForm, AuthorForm, SignUpForm, GendreForm, PublisherForm
from books.models import Ebook, Gendre, Autor, Banner, MainBanner, Cart, CartProduct, Order
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q


pages_in_pagination = 5

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'books/signup.html'


class BookListView(ListView):
    paginate_by = pages_in_pagination
    template_name='books/book_list.html'
    model = Ebook

# class BookDetailView(DetailView):
#     template_name = 'books/book_details.html'
#     model = Ebook
#     pk_url_kwarg = 'ebook_slug'

class BookDetailView(DetailView):
    template_name = 'books/book_details.html'
    model = Ebook
    pk_url_kwarg = 'ebook_slug'


    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)

        ebooks = Ebook.objects.filter(gendre__in=self.object.gendre.all()).exclude(id=self.object.id)
        context_related_list = list(ebooks)
        random.shuffle(context_related_list)
        context_related = context_related_list[0:1]
        context['related'] = context_related
        return context






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
        top_5_rated = Ebook.objects.filter(ratings__isnull=False).order_by('-ratings__average')[0:5]

        return render(request,'books/home.html',{'gendres':gendres,
                                                 'gendre_count':gendre_count,
                                                 'ebooks':ebooks,
                                                 'last5_ebooks':last5_ebooks,
                                                 'discount_books':discount_books,
                                                 'banners':banners,
                                                 'mainbaner':mainbaner,
                                                 'top_5_rated':top_5_rated,
                                                 })

class GendreBooksView(View):
    def get(self,request,gendre_slug=None):
        gendre_books = Ebook.objects.all()
        if gendre_slug:
            gendre= Gendre.objects.get(slug=gendre_slug)
            gendre_books=gendre_books.filter(gendre=gendre)
            paginator = Paginator(gendre_books,pages_in_pagination)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request,'books/gendre_list.html',{'gendre_books':gendre_books,'gendre':gendre,'page_obj':page_obj})



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


class PromoBooksList(ListView):
    paginate_by = pages_in_pagination
    context_object_name = 'promo_books'
    queryset = Ebook.objects.filter(discount_percent__gt=0)
    template_name = 'books/promo_books.html'

class AuthorBooksView(View):
    def get(self,request,autor_slug=None):
        autor_books = Ebook.objects.all()
        if autor_slug:
            autor = Autor.objects.get(slug=autor_slug)
            autor_books=autor_books.filter(autor=autor)
            paginator = Paginator(autor_books,pages_in_pagination)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, 'books/author_list.html', {'autor_books': autor_books,'autor':autor,'page_obj':page_obj})


class NewBooksList(ListView):
    paginate_by = pages_in_pagination
    context_object_name = 'new_books'
    queryset = Ebook.objects.order_by('-created')
    template_name = 'books/new_books.html'


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

class OrderView(LoginRequiredMixin,View):

    def get(self, request):
        cart= Cart.objects.get(user=request.user)
        order_details = Order.objects.create(
        user=request.user,
        total=cart.cart_total()
        )
        order_details.save()
        order_details.product.set(cart.product.all())
        order_details.save()
        cart.delete()

        return render(request,'books/order_placed.html',context={'order_details':order_details})

class MyEbooks(LoginRequiredMixin,View):
    def get(self,request):
        # order_paid = Order.objects.filter(user=request.user).filter(payment_status=True)
        return render(request,'books/my_books.html')


class OrderHistory(LoginRequiredMixin,View):
    def get(self,request):
        order_history = Order.objects.filter(user=request.user).order_by('-order_date')
        return render(request,'books/order_history.html',{'order_history':order_history})

# class BestRated(View):
#     def get(self,request):
#         top_10_rated = Ebook.objects.filter(ratings__isnull=False).order_by('-ratings__average')[0:10]
#         return render(request,'books/top10.html',{'top_10_rated',top_10_rated})

class BestRated(ListView):
    context_object_name = 'new_books'
    queryset = Ebook.objects.filter(ratings__isnull=False).order_by('-ratings__average')[0:10]
    template_name = 'books/top10.html'