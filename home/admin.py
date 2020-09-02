from django.contrib import admin
from .models import Category, TAPE_TITLE, Othermovies, Movie1, Tv1, Trailers, Cart, Checkout, Checkout2
# Register your models here.

admin.site.register(Category)
admin.site.register(TAPE_TITLE)
admin.site.register(Othermovies)
admin.site.register(Movie1)
admin.site.register(Tv1)
admin.site.register(Trailers)
admin.site.register(Cart)
admin.site.register(Checkout)
admin.site.register(Checkout2)

