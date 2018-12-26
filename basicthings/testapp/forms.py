from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.forms import UserChangeForm


#related to registration
# from django.contrib.auth.forms import UserCreationForm
# class RegistrationForm(UserCreationForm):
#     email=forms.EmailField(required=True)
#
#     class Meta:
#         model=User
#         fields =('username','first_name','last_name','email','password1','password2')
#
#     def save(self, commit=True):
#         user = super(RegistrationForm,self).save(commit=False)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
#
#         if commit:
#             user.save()
#
#         return user




#Customisation of register form
class UserCreationForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter username'
                }),required=True,max_length=50)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'}
    ), required=True, max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Lastname'}
    ), required=True, max_length=50)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Email'}
    ), required=True, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your password'}
    ), required=True, max_length=50)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}
    ), required=True, max_length=50,help_text="Enter the same password as above for verification.")




    class Meta:
        model=User
        fields=('username','first_name','last_name')




    def clean_username(self):
        user = self.cleaned_data['username']
        try:
            match =User.objects.get(username = user)
        except:
            return self.cleaned_data['username']
        raise forms.ValidationError("Username already exsits")


    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            mt= validate_email(email)
        except:
            return forms.validationError('Email not in correct form')
        return email
    # def check_email(self):
    #     # Get the email
    #     email = self.cleaned_data.get('email')
    #
    #     # Check to see if any users already exist with this email as a username.
    #     try:
    #         match = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         # Unable to find a user, this is fine
    #         return email
    #
    #     # A user was found with this as a username, raise an error.
    #     raise forms.ValidationError('This email address is already in use.')

    def clean_confirm_password(self):
        pswd = self.cleaned_data['password']
        cpswd= self.cleaned_data['confirm_password']
        MIN_LENGTH =8

        if pswd and cpswd:
            if pswd != cpswd:
                raise forms.ValidationError('Both passwords should match')
            else:
                if len(pswd) < MIN_LENGTH:
                    raise forms.ValidationError("Your password must contain at least %d characters" %MIN_LENGTH)

                if pswd.isdigit():
                    raise forms.ValidationError("Your password can't be entirely numeric")








class EditProfileForm(UserChangeForm):

    class Meta:
        model=User
        fields=['first_name','last_name','email','password']



