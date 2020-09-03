from django import forms
from .models import Checkout

class CheckoutForm1(forms.Form):
    Username = forms.CharField(initial='Henry Cavill')
    email = forms.CharField(max_length=50, initial='synder@wb.com')
    Address = forms.CharField(max_length=50)
    City = forms.CharField(max_length=50)
    State = forms.CharField(max_length=50)
    Zip = forms.CharField(max_length=50)
    NameOnCard = forms.CharField(max_length=50)
    CCNumber = forms.IntegerField()
    ExpDate = forms.DateField(widget=forms.SelectDateWidget)
    # ExpYear = forms.CharField()

# RawForm
class CheckoutForm2(forms.Form):
    Username = forms.CharField(initial='Henry Cavill')
    email = forms.CharField(max_length=50, initial='synder@wb.com')
    Address = forms.CharField(max_length=50)
    City = forms.CharField(max_length=50)
    State = forms.CharField(max_length=50)
    Zip = forms.CharField(max_length=50)
    NameOnCard = forms.CharField(max_length=50)
    CCNumber = forms.IntegerField()
    ExpDate = forms.DateField(widget=forms.SelectDateWidget)
    # ExpYear = forms.CharField()


