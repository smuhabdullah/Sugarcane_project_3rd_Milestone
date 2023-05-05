from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class CustomPasswordWidget(forms.TextInput):
    input_type = 'password'

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name =  forms.CharField(label='Last Name', max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email Address', required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email']


    
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    password1 = forms.CharField(
        label='Password',
        widget=CustomPasswordWidget(
            attrs={
                # 'placeholder': 'Enter Password',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=CustomPasswordWidget(
            attrs={
                # 'placeholder': 'Confirm Password',
                'autocomplete': 'off',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    # 'placeholder': 'Enter Username',
                    'class': 'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    # 'placeholder': 'Enter Email',
                    'class': 'form-control'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add labels to form inputs
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email'
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email


