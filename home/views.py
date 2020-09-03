from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import django_filters


# Create your views here.
from django.views.generic import View, DetailView
from .models import *
from .forms import CheckoutForm1, CheckoutForm2

class BaseView(View):
    view = {}

class view1(BaseView):
    def get(self,request):
        self.view['TapeT'] = TAPE_TITLE.objects.all()
        # self.view['Hall'] = Movie1.objects.all()
        self.view['Hall1'] = Movie1.objects.filter(Rank=1)
        self.view['Hall2'] = Movie1.objects.filter(Rank=2)
        self.view['Hall3'] = Movie1.objects.filter(Rank=3)
        # self.view['TV'] = Tv1.objects.all()
        self.view['TV1'] = Tv1.objects.filter(Rank=1)
        self.view['TV2'] = Tv1.objects.filter(Rank=2)
        self.view['TV3'] = Tv1.objects.filter(Rank=3)
        self.view['Demo'] = Trailers.objects.all()
        return render(self.request,'index.html',self.view)

# class view2(BaseView):
#     def get(self,request):
#         return render(self.request,'moviesingle.html', self.view)

class MovieDetailView(DetailView):
     model = Movie1
     template_name = 'moviesingle.html'



class SeriesDetailView(DetailView):
    model = Tv1
    template_name = 'seriessingle.html'

class MovieGenre(BaseView):
    def get(self,request):
        # self.view['Genre1'] = Movie1.objects.filter(MoviesGenre=('SH','ACT','COM','SCI-FY','ANI','DR','HOR','ADV' ))
        self.view['Genre1'] = Movie1.objects.filter(MoviesGenre__contains = 'SH')
        self.view['Genre2'] = Movie1.objects.filter(MoviesGenre__contains='ACT')
        self.view['Genre3'] = Movie1.objects.filter(MoviesGenre__contains='COM')
        self.view['Genre4'] = Movie1.objects.filter(MoviesGenre__contains='SCI-FY')
        self.view['Genre5'] = Movie1.objects.filter(MoviesGenre__contains='ANI')
        self.view['Genre6'] = Movie1.objects.filter(MoviesGenre__contains='DR')
        self.view['Genre7'] = Movie1.objects.filter(MoviesGenre__contains='HOR')
        self.view['Genre8'] = Movie1.objects.filter(MoviesGenre__contains='ADV')

        return render(self.request, 'MovieGenre.html', self.view)

    # GENRE = (('ACT', 'ACTION'), ('ADV', 'ADVENTURE'), ('COM', 'COMEDY'), ('SCI-FY', 'SCI-FY'), ('ANI', 'ANIMATITON'),
    #          ('HOR', 'HORROR'), ('SH', 'SUPERHERO'), ('DR', 'DRAMA'))


# class MovieGenre(django_filters.FilterSet):
#    MoviesGenre = django_filters.ChoiceFilter(choices=GENRE)
#    class Meta:
#       model = Movie1
#       fields = ['MoviesGenre']


class TvGenre(BaseView):
    def get(self,request):
        self.view['Genre1'] = Tv1.objects.filter(SeriesGenre__contains='SH')
        self.view['Genre2'] = Tv1.objects.filter(SeriesGenre__contains='ACT')
        self.view['Genre3'] = Tv1.objects.filter(SeriesGenre__contains='COM')
        self.view['Genre4'] = Tv1.objects.filter(SeriesGenre__contains='SCI-FY')
        self.view['Genre5'] = Tv1.objects.filter(SeriesGenre__contains='ANI')
        self.view['Genre6'] = Tv1.objects.filter(SeriesGenre__contains='DR')
        self.view['Genre7'] = Tv1.objects.filter(SeriesGenre__contains='HOR')
        self.view['Genre8'] = Tv1.objects.filter(SeriesGenre__contains='ADV')
        return render(self.request,'TvGenre.html', self.view)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']

        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'Username is already taken')
                return render(request, 'register.html')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'This email has already been used to create account.')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password
                 )
                user.save()
                messages.success(request,'You have been successfully registered.')
                return render(request, 'register.html')
        else:
                messages.error(request,'Password does not match.')
                return render(request, 'register.html')

    return render(request, 'register.html')


@login_required
def cart(request,slug):
    if Cart.objects.filter(slug = slug).exists():
        quantity = Cart.objects.get(slug = slug).quantity
        quantity += 1
        price = Movie1.objects.get(slug = slug).Price
        Cart.objects.filter(slug=slug).update( Price = price)
        Cart.objects.filter(slug=slug).update( quantity = quantity)
    else:
        username = request.user
        data = Cart.objects.create(
        user = username,
        slug = slug
        )
        data.save()
    return redirect('home:mycart')

def deletecart(request,slug):
    if Cart.objects.filter(slug = slug).exists():
        Cart.objects.filter(slug=slug).delete()
    return redirect('home:mycart')


def removecart(request,slug):
    if Cart.objects.filter(slug = slug).exists():
        quantity = Cart.objects.get(slug = slug).quantity
        quantity -= 1
        Cart.objects.filter(slug=slug).update( quantity = quantity)
    return redirect('home:mycart')

class CartView(BaseView):
    def get(self,request):
       self.view['slugs'] = Cart.objects.filter(checkout = False, user = request.user)
       self.view['cart_movies'] = Movie1.objects.all()
       return render(request,'cart.html',self.view)


class SearchView(BaseView):
    def get(self,request):
        query = request.GET.get('query',None)
        if not query:
            return redirect('/')

        self.view['search_Movie'] = Movie1.objects.filter(Title__icontains = query)
        return render(request,'searchMovies.html',self.view)

class SearchView1(BaseView):
    def get(self,request):
        query = request.GET.get('query',None)
        if not query:
            return redirect('/')

        self.view['search_Series'] = Tv1.objects.filter(Title__icontains = query)
        return render(request,'searchSeries.html',self.view)

# @login_required
class CheckoutView(BaseView):
    def get(self, request):
        self.view['final'] = Cart.objects.filter(checkout = False, user= request.user)
        # Movie1.slug == Cart.slug
        self.view['final_movies'] = Movie1.objects.filter()
        # final = Movie1.objects.all(request.Price)
        return render(request, 'checkout.html', self.view)
        # self.view['slugs'] = CartView.objects.all(user=request.user)

    # def post(self, *args, **kwargs):
    #     form = CheckoutForm(self.request.POST or None)
    #     if form.is_valid():
    #         print("The form is valid")
    #         return redirect('Checkout')
    #     messages.warning(self.request, 'Form not submitted')
    #     return redirect('Checkout')

# def totalprice(request,slug):
#     TotalPrice = 0
#     if Cart.objects.exists:
#         Price = Cart.objects.get(slug = slug).price
#         TotalPrice += Price
#         Cart.objects.get(TotalPrice = TotalPrice).update()
#     return TotalPrice
# class CheckoutView(BaseView):
#     def total(request,slug):
#          return redirect('home:Checkout')

# def checkoutformView(request):
#     form = CheckoutForm1(request.POST)
#     if form.is_valid():
#         form.save()
#     context = {
#         'form':form
#     }
#     return render(request,'checkout.html',context)

# def checkoutformView(request):
#     context = {}
#     return render(request,'checkout.html',context)

# def checkoutformView(request):
#     my_form = CheckoutForm1()
#     if request.method == 'POST':
#         my_form = CheckoutForm1(request.POST)
#         if my_form.is_valid():
#             # Checkout.objects.create(**my_form.cleaned_data)
#             Username = my_form.CharField['username']
#             email = my_form.CharField['username']
#             Address = my_form.CharField['Address']
#             City = my_form.CharField['City']
#             State = my_form.CharField['State']
#             Zip = my_form.CharField['Zip']
#             NameOnCard = my_form.CharField['NameOnCard']
#             CCNumber = my_form.IntegerField['CCNumber']
#             ExpMonth = my_form.CharField['ExpMonth']
#             ExpYear = my_form.CharField['ExpYear']
#
#             print(Username,email,Address,City,State,Zip,NameOnCard, CCNumber, ExpMonth, ExpYear)
#
#
#         else:
#             print(my_form.errors)
#
#     context = {
#         "form":my_form
#     }
#     return render(request,'Checkout',context)

# def checkoutformView1(request):
#     form = CheckoutForm1()
#     if request.method == 'POST':
#         form = CheckoutForm1(request.POST)
#         if form.is_valid():
#             Checkout.objects.create(**form.cleaned_data)
#             print('Valid')
#     context = {
#         "form":form
#     }
#
#     return render(request,'checkout1.html',context)

# def checkoutformView1(request):
#     template_name = 'checkout1.html'
#     form_class = CheckoutForm1
#     success_url = '/checkout1/'
#
#     return render(request,'checkout1.html')

def checkoutformView2(request):
    form = CheckoutForm2()
    if request.method =="POST":
        form = CheckoutForm2(request.POST)
        if form.is_valid():
            print('form.cleaned_data')
            messages.success(request, 'Thank you! Your items will be delivered soon.')
            Checkout2.objects.create(**form.cleaned_data)
            form= CheckoutForm2()
        else:
            print(form.errors)
    context = {
        "form": form
    }
    return render(request, 'checkout2.html', context)
