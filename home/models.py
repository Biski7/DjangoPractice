from django.conf import settings
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField


AVAILABILITY = (('av', 'available'),('N-av','Not-available'))
GENRE = (('ACT', 'ACTION'),('ADV','ADVENTURE'),('COM','COMEDY'), ('CR','CRIME'), ('SCI-FY','SCI-FY') ,('ANI','ANIMATION'),('HOR','HORROR'), ('SH', 'SUPERHERO'), ('DR','DRAMA'))
STATUS = (('active', 'Active'), ('inactive', 'Inactive'), ('', 'Default'))
FIELDS = (('In Theatre 2020','In Theatre 2020'),('Coming Soon','Coming Soon'),('IMDB RATING','IMDB RATING'))
FIEL = (('POPULAR','POPULAR'),('Coming Soon','Coming Soon'),('RATING','IMDB RATING'))
# Create your models here.

class Category(models.Model):
    Title = models.CharField(max_length=400)
    description = models.TextField(max_length=400)
    slug = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.Title


class TAPE_TITLE(models.Model):
    Title = models.CharField(max_length=500)
    Imdb_rating = models.FloatField(blank=True)
    Rotten_tomatoes_rating = models.FloatField(blank=True)
    Rate_this_movie = models.FloatField(max_length=300,blank=True)
    About = models.CharField(max_length=1000)
    Cast = models.CharField(max_length=1000)
    Release_date = models.IntegerField()
    Status = models.CharField(max_length=100, choices=AVAILABILITY)
    # Image = models.TextField()
    Image = models.ImageField(upload_to='media')
    Genre = MultiSelectField(choices=GENRE,default='basic')

    def __str__(self):
        return self.Title

class Movie1(models.Model):
    Title = models.CharField(max_length=400)
    slug = models.CharField(max_length=500, unique=True)
    About = models.CharField(max_length=1000, default='Its Good')
    Video = models.TextField(max_length=500, default='Not Available')
    # Image = models.TextField(max_length=500, unique=True)
    Image = models.ImageField(upload_to='media')
    Cast = models.TextField(max_length=1000, default='...')
    Rank = models.IntegerField()
    MoviesGenre = MultiSelectField(choices=GENRE)
    Status = models.CharField(max_length=200, choices=STATUS, blank=True)
    Field = models.CharField(max_length=200, choices=FIELDS, blank=False)
    Imdb_rating = models.CharField(max_length=200, blank=True, default='Not Yet Rated')
    # RankB = models.IntegerField(default=1)
    Price = models.IntegerField()



    def __str__(self):
        return self.Title

    def get_movie_url(self):
        return reverse('home:movie', kwargs={'slug':self.slug})

    def add_to_cart(self):
        return reverse('home:cart', kwargs={'slug': self.slug})


class Tv1(models.Model):
    Title = models.CharField(max_length=500)
    slug = models.CharField(max_length=500, unique=True, default=1)
    # Image = models.TextField(max_length=500)
    Image = models.ImageField(upload_to='media')
    About = models.CharField(max_length=1000, default='Its Good')
    Cast = models.TextField(max_length=1000, default='...')
    Rank = models.IntegerField()
    Video = models.TextField(max_length=500, default='Not Available')
    SeriesGenre = MultiSelectField(choices=GENRE)
    Status = models.CharField(max_length=200, choices=STATUS, blank=True)
    Field = models.CharField(max_length=200, choices=FIEL, blank=False, default=1)
    Imdb_rating = models.CharField(max_length=200, blank=True,default='Not Yet Rated')

    def __str__(self):
        return self.Title

    def get_series_url(self):
        return reverse('home:series', kwargs={'slug': self.slug})

class Trailers(models.Model):
    Title = models.CharField(max_length=500)
    # Image = models.TextField(max_length=400)
    Image = models.ImageField(upload_to='media')
    Video = models.TextField(max_length=500)
    Rank = models.IntegerField()
    SeriesGenre = MultiSelectField(choices=GENRE)
    Length = models.TextField(max_length=200)

    def __str__(self):
        return self.Title


class Othermovies(models.Model):
    Title = models.CharField(max_length=500)
    Image = models.ImageField(upload_to='media')
    # Image = models.TextField(max_length=400)
    Rank = models.IntegerField()
    Imdb_rating = models.FloatField()
    MoviesGenre = MultiSelectField(choices=GENRE)
    Status = models.CharField(max_length=200, choices=STATUS, blank=True)

    def __str__(self):
        return self.Title

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug = models.CharField(max_length = 300)
    quantity = models.IntegerField(default=1)
    checkout = models.BooleanField(default=False)
    Price = models.FloatField(default= 100 )
    item = models.ForeignKey(Movie1,on_delete=models.CASCADE, default =1 )

    def __str__(self):
        return f"{self.quantity} of {self.slug}"

    def remove_one_ticket(self):
        return reverse('home:removecart', kwargs={'slug': self.slug})

    def remove_all_tickets(self):
        return reverse('home:deletecart', kwargs={'slug': self.slug})

    def add_one_ticket(self):
        return reverse('home:cart', kwargs={'slug': self.slug})

    def total_price_ticket(self):
        price = 0
        # self.Price = Movie1.objects.get(slug=self.slug).Price
        price = Movie1.objects.get(slug=self.slug).Price
        Cart.objects.filter(slug=self.slug).update(Price=price)
        # self.Price = self.item.Price
        # self.item.slug = self.slug
        # if self.item.slug == self.slug:
        # return self.quantity * self.Price
        return self.quantity * price

    # def total_final_price(self):
    #     total_price = 0
    #     for all in Cart.objects.all():
    #         total_price  += Cart.total_price_ticket(self)
    #     return total_price

    def total_final_price(self):
        total_price = 0
        total = 0
        # price = Movie1.objects.get(slug=self.slug).Price
        # Cart.objects.filter(slug=self.slug).update(Price=price)
        total_price  += Cart.total_price_ticket(self)
        return total_price



    



    # def get_final_price(self):
    #     total = 0
    #     for slug in Cart():
    #         total += Cart.total_price_ticket()
    #     return total
# class Checkout1(models.Model):
        #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        #     Username = models.CharField(max_length=500)
        #     email = models.TextField(max_length=500)
        #     # slug = models.CharField(max_length = 300)
        #     # quantity = models.IntegerField(default=1)
        #     Address = models.CharField(max_length=500)
        #     City = models.CharField(max_length=500)
        #     State = models.CharField(max_length=500)
        #     Zip = models.CharField(max_length=500)
        #     NameOnCard = models.CharField(max_length=500)
        #     CCNumber = models.IntegerField()
        #     ExpMonth = models.DateField()
        #     ExpYear = models.DateField()
        #     # checkout = models.BooleanField(default=False)
        #     # price = models.FloatField(default= 100 )
        #     quantity = models.ForeignKey(Cart, on_delete=models.CASCADE, default=1)
        #     price = models.ForeignKey(Movie1, on_delete=models.CASCADE, default=100)
        #
        #     # slug = models.ForeignKey(Cart,on_delete=models.CASCADE)
        #
        #     def __str__(self):
        #         return self.user.username
    # def get_final_price(self):
    #     total = 0
    #     for slug in Cart():
    #         total += Cart.total_price_ticket()
    #     return total
    #
class Checkout(models.Model):
    Username = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    Address = models.CharField(max_length=500)
    City = models.CharField(max_length=500)
    State = models.CharField(max_length=500)
    Zip = models.CharField(max_length=500)
    NameOnCard = models.CharField(max_length=500)
    CCNumber = models.IntegerField()
    ExpMonth = models.CharField(max_length=20)
    ExpYear = models.CharField(max_length=20)

    def __str__(self):
        return self.Username

class Checkout2(models.Model):
    Username = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    Address = models.CharField(max_length=500)
    City = models.CharField(max_length=500)
    State = models.CharField(max_length=500)
    Zip = models.CharField(max_length=500)
    NameOnCard = models.CharField(max_length=500)
    CCNumber = models.IntegerField()
    ExpMonth = models.CharField(max_length=20)
    ExpYear = models.CharField(max_length=20)

    def __str__(self):
        return self.Username



