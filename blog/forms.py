from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm
from blog.models import Person, Fotografo


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label = 'New Password', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label = 'Repeat Password', widget=forms.PasswordInput())

class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254)
    def clean_email(self):
        email = self.cleaned_data['email']
        test = User.objects.filter(email=email)
        if not test:
            raise forms.ValidationError('Ese correo no lo tenemos registrado')
        return email


class personaForm(forms.ModelForm):

    class Meta:
        model = Person
        #fields = ('phone', 'city', )
        fields = ('__all__')   
        exclude = ('user',)   


class fotografoForm(forms.ModelForm):

    class Meta:
        model = Fotografo
        fields = ('__all__')     
        exclude = ('rutaImagen', 'fotografo','user')   



class createUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'email', 'password1','password2','first_name','last_name' ]

    def clean_email(self):
        print('email')

        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            print('ya existe email')

            raise forms.ValidationError(
                'Este correo ya lo están utilizando.'
            )
        return email

class RegistrationForm(forms.ModelForm):
    
    username = forms.CharField(label ='enter Username',min_length=4, max_length=50, help_text='Required')

    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required':'Sorry, necesitarás ingresar un correo'
    })
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeatr Password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')
    
    #chequea si el usuario ya existe
    def clean_username(self):
        print('username')
        username = self.cleaned_data['username'].lower()
        r  = User.objects.filter(username=username)
        if r.count():
            print('ya existe username')
            raise ValidationError("El usuario ya existe.")
        return username

    #chequea que las claves coincidian
    def clean_password2(self):
        print('paswword')

        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            print('ya existe password')

            raise forms.ValidationError("Contraseñas no coinciden.")
        return cd['password2']
    
    #chequea que el correo ya exista 
    def clean_email(self):
        print('email')

        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            print('ya existe email')

            raise forms.ValidationError(
                'Este correo ya lo están utilizando.'
            )
        return email
    