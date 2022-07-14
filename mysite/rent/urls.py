from django.urls import path
from .views import rental, login_page, register_page, logout_page, \
    cart, book_to_cart, film_to_cart, cd_to_cart
from . import views

app_name = 'rent'
urlpatterns = [
    # path('', home, name='home'),
    path('', views.HomeView.as_view(), name='home'),
    path('/<int:rental_id>', rental, name='rental'),
    path('/cart', cart, name='cart'),
    path('/login', login_page, name='login'),
    path('/register', register_page, name='register'),
    path('/logout', logout_page, name='logout'),
    path('/booktocart/<int:book_id>', book_to_cart, name='book_to_cart'),
    path('/filmtocart/<int:film_id>', film_to_cart, name='film_to_cart'),
    path('/cdtocart/<int:cd_id>', cd_to_cart, name='cd_to_cart')

]
