from django.db import models
from django.utils.translation import gettext as _
from django.contrib import admin
from django.contrib.auth.models import User
from datetime import timedelta


# Create your models here.
PROVINCES = (
    ('DSL', 'dolnośląskie'), ('KP', 'kujawsko-pomorskie'), ('LBL', 'lubelskie'), ('LBU', 'lubuskie'),
    ('LDZ', 'łódzkie'), ('MLP', 'małopolskie'), ('MAZ', 'mazowieckie'), ('OPO', 'opolskie'), ('PKR', 'podkarpackie'),
    ('PDL', 'podlaskie'), ('POM', 'pomorskie'), ('SL', 'śląskie'), ('SW', 'świętokrzyskie'),
    ('WM', 'warmińsko-mazurskie'), ('WLKP', 'wielkopolskie'), ('ZPM', 'zachodniopomorskie')
             )

BOOK_GENRE = (
    ('fantastyka', 'Fantastyka'), ('kryminał', 'Kryminał'), ('popularno-naukowe', 'Popularno-naukowe'),
    ('powieść historyczna', 'Powieść historyczna'), ('romans', 'Romans'), ('thriller', 'Thriller')
)


class Rental(models.Model):
    name = models.CharField(max_length=30)
    street = models.CharField(_('Street'), max_length=30)
    city = models.CharField(_('City'), max_length=30)
    province = models.CharField(_('Province'), choices=PROVINCES, max_length=20)
    postal_code = models.CharField(_('Postal Code'), max_length=6)

    def __str__(self):
        return self.name

    @admin.display(
        ordering='city',
        description='Address'
    )
    def get_address(self):
        return f'{self.city}, ul.{self.street}'


class Book(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    author = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    book_genre = models.CharField(choices=BOOK_GENRE, max_length=30)
    publishing_house = models.CharField(max_length=20)
    ISBN = models.CharField(max_length=17, blank=True)

    date_of_loan = None

    def __str__(self):
        return f'{self.author}, {self.title}'

    @admin.display(
        boolean=True,
        description='Available'
    )
    def check_availability(self):
        if self.date_of_loan is None:
            return True
        else:
            return f'Unavailable, expected date of return: {self.get_expected_date_of_return()}'

    def get_expected_date_of_return(self):
        if self.date_of_loan is not None:
            return (self.date_of_loan + timedelta(days=30)).strftime("%Y-%m-%d")
        else:
            raise Exception('Object is not loaned.')


class Film(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    director = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    film_genre = models.CharField(max_length=20)
    duration = models.DurationField()

    date_of_loan = None

    def __str__(self):
        return f'{self.director, self.title}'

    @admin.display(
        boolean=True,
        description='Available'
    )
    def check_availability(self):
        if self.date_of_loan is None:
            return True
        else:
            return f'Unavailable, expected date of return: {self.get_expected_date_of_return()}'

    def get_expected_date_of_return(self):
        if self.date_of_loan is not None:
            return (self.date_of_loan + timedelta(days=30)).strftime("%Y-%m-%d")
        else:
            raise Exception('Object is not loaned.')


class CD(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    author = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    music_genre = models.CharField(max_length=20)
    track_list = models.TextField()
    duration = models.DurationField

    date_of_loan = None

    def __str__(self):
        return f'{self.author}, {self.title}'

    @admin.display(
        boolean=True,
        description='Available'
    )
    def check_availability(self):
        if self.date_of_loan is None:
            return True
        else:
            return f'Unavailable, expected date of return: {self.get_expected_date_of_return()}'

    def get_expected_date_of_return(self):
        if self.date_of_loan is not None:
            return (self.date_of_loan + timedelta(days=30)).strftime("%Y-%m-%d")
        else:
            raise Exception('Object is not loaned.')


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class Cart(models.Model):
    customer = models.OneToOneField(Customer, null=True, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    films = models.ManyToManyField(Film)
    cds = models.ManyToManyField(CD)

    def __str__(self):
        return str(self.customer)
