from django.core.validators import ip_address_validator_map
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.utils.encoding import *
from django.utils.http import * 
from django.http import HttpResponse, request

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView

from .serializers import PostSerializer, PostPictureSerializer
from .models import Person, Post, PostPicture, postCategory, Fotografo
from .forms import RegistrationForm, fotografoForm, createUserForm, personaForm

from .token import account_activation_token


def registerPage(request):
  form = UserCreationForm()
  photografoForm = fotografoForm()


  context = {
    'registerForm' : form, 
    'photografoForm' : photografoForm, 
  }
  return render(request,'accounts/sign-up2.html', context)


class blogList(APIView):
  """
  A viewset for viewing and editing user instances.
  """
  renderer_classes = [TemplateHTMLRenderer]
  template_name = 'blog/blog.html'
  ordering_fields = ['created_on']


  def get(self, request):
    queryset = Post.objects.all()
    serializer = PostSerializer(queryset, many=True)

    return Response({'posts': serializer.data,
                    'category' : postCategory.objects.all()})
  
class blogFiltred(APIView):
  """
  A viewset for viewing and editing user instances.
  """
  renderer_classes = [TemplateHTMLRenderer]
  template_name = 'blog/blog.html'

  def get(self, request, id):
    queryset = Post.objects.filter(category = id)
    serializer = PostSerializer(queryset, many=True)
    return Response({'posts': serializer.data,
                    'category' : postCategory.objects.all()})



class blogList2(ListView):
    paginate_by = 10
    model = Post
    template_name = "blog/blog.html"
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["PostPicture"] =  PostPicture.objects.all()
            queryset = Post.objects.all()
            serializer = PostSerializer(queryset, many=True)
            context['posts']= serializer.data
            
            return context    

    


#def blogview(request):

#  return render(request, 'blog/blog.html')

def testingIndex(request):
    registerForm = RegistrationForm()
    queryset = Post.objects.all()
    serializer = PostSerializer(queryset, many=True)
    context = {
      'form' : registerForm,
      'posts' : serializer.data,
      }
    return render(request,"blog/index.html",context)


class PostDetail(APIView):
  """
  A viewset for viewing and editing user instances.
  """
  renderer_classes = [TemplateHTMLRenderer]
  template_name = 'post/detail-public.html'

  def get(self, request, id):
    post = get_object_or_404(Post, id=id)
    serializer = PostSerializer(post)
    return Response({'serializer': serializer, 'post': post})

class LoginFormView(LoginView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Iniciar sesión'
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
          return redirect('backoffice:backoffice')
  
        return super().dispatch(request, *args, **kwargs)


    

#ViewSets define the view behavior.


# class CreatePostView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'create-post.html'

#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         # postpictures_form = PostPicturesFormSet(self.request.POST)
#         if (form.is_valid() ):
#           return self.form_valid(form, )
#         else:
#           return self.form_invalid(form, )

#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.author = self.request.person
#         # postpictures_form.instance = obj
#         # postpictures_form.save()
#         obj.save()
#         return reverse('posts')

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))



'''class PostList(APIView):
  """
  A viewset for viewing and editing user instances.
  """
  renderer_classes = [TemplateHTMLRenderer]
  template_name = 'blog/index.html'
  ordering_fields = ['created_on']

  def get(self, request):
    queryset = Post.objects.all()
    serializer = PostSerializer(queryset, many=True)
    return Response({'posts': serializer.data})

class PostDetail(APIView):
  """
  A viewset for viewing and editing user instances.
  """
  renderer_classes = [TemplateHTMLRenderer]
  template_name = 'blog/detail.html'

  def get(self, request, id):
    post = get_object_or_404(Post, id=id)
    serializer = PostSerializer(post)
    return Response({'serializer': serializer, 'post': post})
'''

"""
def login_view(request):
  if request.method == "POST":
    username = request.POST.get("username")
    password = request.POST.get("password")

      
    user = authenticate(request, username = username, password= password)

    if user is not None:
      login(request, user)
      return redirect("backoffice")
        
    else:
      print("user doesnt exist")
      messages.info(request, 'Username or password is incorrect')

  return render(request, "login.html")

"""
  #testing pagina
def testing_website(request):
    return render(request,"trying.html")


def accounts_register(request):
  registerForm = createUserForm()
  personForm = personaForm()
  photografoForm = fotografoForm()
  print('beforepost')
  if request.method =="POST":
      registerForm = createUserForm(request.POST) 
      personForm = personaForm(request.POST)
      print("post ")
      print()
      if registerForm.is_valid() and personForm.is_valid():
        user = registerForm.save(commit=False)        
        user.email = registerForm.cleaned_data['email']
        user.set_password(registerForm.cleaned_data['password1'])
        user.is_active = False

        
        phone = personForm.cleaned_data['phone']
        city= personForm.cleaned_data['city']
        region = personForm.cleaned_data['region']
        genero = personForm.cleaned_data['genero']
        newPerson = Person(phone = phone, city= city, region = region, genero=genero)
        newPerson.user = user


        if 'saveFotografo' in request.POST:
              print("es trabajador")
              photografoForm = fotografoForm(request.POST)
             
              print(photografoForm.is_valid())
              if photografoForm.is_valid():
                print("ingresar datos del trabajadorsh")
                instagram = photografoForm.cleaned_data['instagram']
                portafolio = photografoForm.cleaned_data['portafolio']
                idioma = photografoForm.cleaned_data['idioma']
                categoria = photografoForm.cleaned_data['categoriasEspecialidad']
                disponibilidad  = photografoForm.cleaned_data['disponibilidad']
                newFotografo = Fotografo(instagram =instagram, portafolio = portafolio, idioma= idioma, categoriasEspecialidad = categoria, disponibilidad=disponibilidad)
                print(newFotografo)
                user.save()     
                newPerson.is_fotografo = True
                newPerson.save()
                newFotografo.user = user 
                newFotografo.fotografo = 0 
                newFotografo.save()

                current_site = get_current_site(request)
                subject = 'Activa tu cuenta'
                message = render_to_string('accounts/account_activation_email.html',{
                  'user':user,
                  'domain': current_site.domain,
                  'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                  'token': account_activation_token.make_token(user),
                })
                user.email_user(subject=subject,message=message)
                messages.success(request, 'Tu cuenta se ha creado y te hemos enviado un correo de activación')

              else:
                for field in photografoForm:
                   print("Field Error:", field.name,  field.errors)
                messages.warning(request, 'te faltó ingresar datos ')
                  
        else:

            user.save()    
            newPerson.save()
      
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta'
            message = render_to_string('accounts/account_activation_email.html',{
              'user':user,
              'domain': current_site.domain,
              'uid':urlsafe_base64_encode(force_bytes(user.pk)),
              'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject,message=message)
            messages.success(request, 'Tu cuenta se ha creado y te hemos enviado un correo de activación')
      else:
        for field in personForm:
          print("Field Error:", field.name,  field.errors)
        for field in registerForm:
          print("Field Error:", field.name,  field.errors)

  context = {'registerForm' : registerForm ,
      'personaForm' : personForm,
      'fotografoForm' : photografoForm, }
  
  #return render(request,'accounts/sign-up.html',{'registerForm' : registerForm})
  return render(request,'accounts/sign-up2.html', context)


def activate(request,uidb64,token):
    try:
      uid = force_text(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)
    except(TypeError, ValueError,OverflowError, User.DoesNotExist):
      user= None
    if user is not None and account_activation_token.check_token(user, token):
      user.is_active = True
      user.save()
      login(request, user)
      messages.success(request,'Tu cuenta se ha activado!')
      return(redirect('blog:login'))
    

    else:
      messages.error(request,'Error en activar tu cuenta')
      return (redirect('blog:login'))


def terms(request):  
  return render(request,'blog/terms.html')


def workwithus(request):
  return render(request,'registration/register.html')


class Error404view(TemplateView):
    template_name = 'blog/error_404.html'

class Error505view(TemplateView):
    template_name = 'blog/error_505.html'
    
    @classmethod
    def as_error_view(cls):
      v = cls.as_view()
      def view(request):
        r =v(request)
        r.render()
        return r
      return view

def sobreNosotros(request):
  return render(request,'blog/aboutus.html')
  