from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django import forms
from .models import Customer,Product
from django.contrib.auth import password_validation



class CustomerRegistrationForm(UserCreationForm):
  email = forms.CharField(label='Email',help_text='Required. Enter a valid email address.',required=True,widget=forms.EmailInput(attrs={'class':'w-full mb-2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400'}))
  password1 = forms.CharField(label='Password',required=True,widget=forms.PasswordInput(attrs={'class':'w-full mb-2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400'}))
  password2 = forms.CharField(label='Confirm Password',required=True,widget=forms.PasswordInput(attrs={'class':'w-full mb-2 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400'}))

  class Meta:
    model = User
    fields = ('username','email','password1','password2')
    widgets = {'username':forms.TextInput(attrs={'class':'mb-2 w-full px-4 py-2 border rounded-lg m-2 focus:outline-none focus:ring-2 focus:ring-indigo-400'})}
  
class CustomerProfileForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ('customer_name','customer_phone','customer_address','customer_city','customer_state','customer_country')
    labels = {'customer_name':'Full Name','customer_phone':'Phone','customer_address':'Address','customer_city':'City','customer_state':'State','customer_country':'Country'}
    widgets = {'customer_name':forms.TextInput(attrs={'class':'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),
    'customer_phone':forms.NumberInput(attrs={'class':'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),
    'customer_address':forms.TextInput(attrs={'class':'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),
    'customer_city':forms.TextInput(attrs={'class':'block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),
    'customer_state':forms.Select(attrs={'class':'block w-full appearance-none bg-white border border-gray-300 rounded-md py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm'}),
    'customer_country':forms.Select(attrs={'class':'h-full rounded-md border-0 bg-transparent bg-none py-0 pl-4 pr-9 text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm'}),
    
    }

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Current Password', widget=forms.PasswordInput(attrs={'class':'my-2 w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'}))
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class':'my-2 w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'}))
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class':'my-2 w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254,widget=forms.EmailInput(attrs={'class':'my-2 w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'}))

class MySetPasswordReset(SetPasswordForm):
  new_password1 = forms.CharField(strip=False,label=_('New Password'),widget=forms.PasswordInput(attrs={'class':'my-2 w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600','autocomplete':'new-password'}),help_text=password_validation.password_validators_help_text_html())
  new_password2 = forms.CharField(strip=False,label=_('Confirm Password'),widget=forms.PasswordInput(attrs={'class':'my-2 w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600','autocomplete':'new-password'}))


class TailwindFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'appearance-none shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-indigo-400'

class ProductForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name', 'description', 'selling_price', 'discounted_price', 'brand', 'product_quantity',
            'highlight_product_image', 'front_product_image', 'back_product_image', 'rightside_product_image', 'leftside_product_image',
            'colors', 'category','manufactured_by'
        ]
        widgets = {
            'colors': forms.CheckboxSelectMultiple(),
        }