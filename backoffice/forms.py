from django import forms
from django.forms import inlineformset_factory
from blog.models import Post, PostPicture , Person, Fotografo
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title','content','precontent','category')

   
class PicturesForm(forms.ModelForm):
  class Meta:
    model = PostPicture
    fields = ('image','image_name')

    widget = {
      'pictures': forms.ImageField(label='image')
    }

# PostPicturesFormSet = inlineformset_factory(Post, 
#   PostPicture,
#   fields=('image', 'image_name'),
#   extra=1,
#   max_num=1,
#   widgets={
#     'image_name':
#     forms.TextInput(attrs={'placeholder': 'Image name'})
#   }
# )


class UserLoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput())
  password = forms.CharField(widget=forms.PasswordInput())


class UserEditForms(forms.ModelForm):
  first_name= forms.CharField(min_length = 4, max_length=50, label = "First Name")
  last_name= forms.CharField(min_length=4, max_length=50, label = "Last name")
  email = forms.EmailField(max_length=200, label = "Email address")

  class Meta:
    model = User
    fields= ('first_name', 'last_name', 'email')

  def clean_email(self):
    email = self.cleaned_data['email']
    current_user =  self.instance.pk

    if User.objects.filter(email=email).exists():
      try:
        if current_user != User.objects.get(email=email).id:
          raise forms.ValidationError(
            'Este correo ya está siendo utilizado, porfavor ingresa otro correo'
          )
      except User.MultipleObjectsReturned:
         raise forms.ValidationError(
            'Tu correo ha sido creado varias veces ojo ahí'
          )

    return email

class PersonaEditForm(forms.ModelForm):
  class meta:
    models = Person


class FotografoEditForm(forms.ModelForm):
  class meta:
    models = Fotografo

    
  
class PwdChangeForm(PasswordChangeForm):
  old_password = forms.CharField(label = 'Contraseña Actual',widget=forms.PasswordInput())
  new_password1 = forms.CharField(label='Nueva contraseña',widget=forms.PasswordInput())
  new_password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput())

