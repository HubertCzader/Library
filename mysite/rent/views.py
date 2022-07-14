from django.shortcuts import get_object_or_404, render
from .models import Rental, Customer, Book, Film, CD, Cart
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm, CreateCustomerForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic



class HomeView(generic.ListView):
    template_name = 'rent/home.html'
    context_object_name = 'rentals'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Rental.objects.all()


def rental(request, rental_id):
    rent = get_object_or_404(Rental, pk=rental_id)
    books = rent.book_set.all()
    films = rent.film_set.all()
    cds = rent.cd_set.all()
    context = {'books': books, 'films': films, 'cds': cds}
    return render(request, 'rent/rental.html', context)


# def cart(request):
#     if request.user.is_authenticated:
#         return render(request, 'rent/cart.html')
#     else:
#         return redirect('/rent')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/rent')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("working")
                login(request, user)
                return redirect('/rent')
        return render(request, 'rent/login.html')


def logout_page(request):
    logout(request)
    return redirect('/rent')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        cust_form = CreateCustomerForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            cust_form = CreateCustomerForm(request.POST)
            if form.is_valid() and cust_form.is_valid():
                user = form.save()
                customer = cust_form.save(commit=False)
                customer.user = user
                customer.save()
                return redirect('login')
        context = {
            'form': form,
            'cust_form': cust_form,
        }
        return render(request, 'rent/register.html', context)


# def cart(request):
#     if request.user.is_authenticated:
#         car = Customer.objects.all()
#         return render(request, 'rent/cart.html', {'cart': car})
#     else:
#         return redirect('/rent')


def cart(request):
    cust = Customer.objects.filter(user=request.user)
    for c in cust:
        carts = Cart.objects.all()
        for car in carts:
            if car.customer == c:
                context = {
                    'cart': cart
                }
                return render(request, 'rent/cart.html', context)

#
# def book_to_cart(request, book_id):
#     book = Book.objects.get(id=book_id)
#     cust = Customer.objects.filter(user=request.user)
#     Book.date_of_loan = timezone.now()
#
#     for c in cust:
#         carts = Cart.objects.all()
#         req_cart = ''
#         for car in carts:
#             if car.customer == c:
#                 req_cart = car
#                 break
#         if req_cart == '':
#             req_cart = Cart.objects.create(
#                 customer=c,
#             )
#         req_cart.books.add(book)
#     return redirect('/rent/cart')


def book_to_cart(request, book_id):
    if request.user.is_authenticated():
        book = get_object_or_404(Book, pk=book_id)
        cart, created = Cart.objects.get_or_create(user=request.user, active=True)
        cart.add_to_cart(book_id)
        return redirect('/rent/cart')
    else:
        return redirect('/rent')


def film_to_cart(request, film_id):
    film = Film.objects.get(id=film_id)
    cust = Customer.objects.filter(user=request.user)
    Film.date_of_loan = timezone.now()
    for c in cust:
        carts = Cart.objects.all()
        req_cart = ''
        for car in carts:
            if car.customer == c:
                req_cart = car
                break
        if req_cart == '':
            req_cart = Cart.objects.create(
                customer=c,
            )
        req_cart.films.add(film)
    return redirect('/rent/cart')


def cd_to_cart(request, cd_id):
    cd = CD.objects.get(id=cd_id)
    cust = Customer.objects.filter(user=request.user)
    CD.date_of_loan = timezone.now()

    for c in cust:
        carts = Cart.objects.all()
        req_cart = ''
        for car in carts:
            if car.customer == c:
                req_cart = car
                break
        if req_cart == '':
            req_cart = Cart.objects.create(
                customer=c,
            )
        req_cart.cds.add(cd)
    return redirect('/rent/cart')