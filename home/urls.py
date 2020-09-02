from django.urls import path
from .views import view1,MovieDetailView, SeriesDetailView, MovieGenre, TvGenre, signup, cart, CartView, deletecart, CheckoutView, removecart, SearchView, SearchView1,checkoutformView1, checkoutformView2
# from .views import view2
app_name = 'home'

urlpatterns = [
    path('',view1.as_view(), name='home'),
    path('mGenre/',MovieGenre.as_view(), name='mgenre'),
    # path('mGenre/',MovieGenre, name='mgenre'),
    path('tGenre/',TvGenre.as_view(), name='tgenre'),
    # path('try/',Try, name='try'),
    # path('moviesingle.html/', view2.as_view(), name ='moviesingle')
    path('movie/<slug>',MovieDetailView.as_view(), name='movie'),
    path('series/<slug>',SeriesDetailView.as_view(), name='series'),
    path('search',SearchView.as_view(), name='search'),
    path('search1',SearchView1.as_view(), name='search1'),
    path('cart/<slug>',cart, name='cart'),
    path('signup',signup,name= 'signup'),
    path('mycart',CartView.as_view(),name= 'mycart'),
    path('removecart/<slug>',removecart,name= 'removecart'),
    path('deletecart/<slug>',deletecart,name= 'deletecart'),
    path('Checkout', CheckoutView.as_view(), name='Checkout'),
    path('Checkout1', checkoutformView1,name='Checkout1'),
    path('Checkout2', checkoutformView2,name='Checkout2'),
]