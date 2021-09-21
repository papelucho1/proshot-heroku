from blog.forms import fotografoForm, personaForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.template.loader import render_to_string
from blog.models import Person, Post, PostPicture, Fotografo
from .forms import PostForm, PicturesForm, UserEditForms, PersonaEditForm, FotografoEditForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib import messages
from django.forms import modelformset_factory

# Create your views here.

def sendEmail(email):
    try:
        mailServer = smtplib.SMTP('smtp.gmail.com',587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        #settings.EMAIL_HOST_USER , settings.EMAIL_HOST_PASSWORD    
        mailServer.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        
        # Construimos el mensaje simple
        mensaje = MIMEMultipart()

        mensaje['From']=settings.EMAIL_HOST_USER   #settings.EMAIL_HOST_USER 
        mensaje['To']= email
        mensaje['Subject']="Tienes un correo"

        usuario = User.objects.get(email = email)
        content = render_to_string('test/emailTest.html',{'user':usuario})
        mensaje.attach(MIMEText(content,"html"))
        mailServer.sendmail(settings.EMAIL_HOST_USER, #settings.EMAIL_HOST_USER
                email,
                mensaje.as_string())
    except Exception as e:
        return e
    else:
        return True
    



@login_required
def index(request):
    print("back office")
    print(request.user)
    
    try:
        userLogged = request.user
        print(userLogged.person.is_fotografo)
        if userLogged.is_staff:
            return render(request, "backoffice/dashboard.html")

        if userLogged.person.is_fotografo or not userLogged.person.is_fotografo :
            #return render(request, "backoffice/.html")
            return HttpResponseRedirect(reverse_lazy('backoffice:profile'))
        
            
    except Person.DoesNotExist:
        print(request.user.is_staff)
        
        return render(request, "backoffice/dashboard.html")
    

#dashboard admin

#dashboard fotografo

#dashboard usuarios normales

"""
@login_required
#solo admin
def usuarios(request):
    print("back office")
    return render(request, "backoffice/users.html")
"""

#solo admin

class usuariosViews(TemplateView):
    model = User
    template_name = 'backoffice/users.html'
    @method_decorator([login_required,staff_member_required])
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        
        context['personas'] = User.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data ={}
        try:
            if request.method =="POST":
                emails = json.loads(request.POST.get('emails'))   
                print(emails)               
                for email in emails:
                    print(email)
                    if sendEmail(email): 
                        print('correo enviado a', email)
                        
                        continue
                        
                        
                    else:
                        data = {'foo': 'bar'}

        except Exception as e:
            data['error'] = str(e)
       

        return JsonResponse(data)
        
    
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(""))

@login_required
def not_ready(request):
    return render(request, "backoffice/not_ready.html")


#actualiza los datos de la tabla usuarios 
@login_required
def profile(request):
    #iniciar forms que vienen de la página
    user_form = UserEditForms(instance= request.user)
    password_form = PasswordChangeForm(request.user)
    persona_data = Person()
    try:
        persona_data = Person.objects.get(user=request.user) 
        persona_form = personaForm(instance = persona_data)
        
    except Person.DoesNotExist:
        persona_form = personaForm()
        persona_data.user  = request.user
        persona_data.save()
    try:
        fotografo_data = Fotografo.objects.get(user = request.user)
        fotografo_form = fotografoForm(instance=fotografo_data)
    except Fotografo.DoesNotExist:
        fotografo_form = fotografoForm()
    #persona_form = PersonaEditForm()
    if request.method == "POST":
       #actualiza datos
        if "saveDetails" in request.POST:
            print("saveDetails")
         
            user_form = UserEditForms(instance = request.user,
                                    data = request.POST)
            print('userform selected')
            #print(user_form)
            persona_form = personaForm(request.POST)
            if user_form.is_valid() and persona_form.is_valid():

               user_form.save()
               phone = persona_form.cleaned_data['phone']
               city = persona_form.cleaned_data['city']
               region = persona_form.cleaned_data['region']
               genero = persona_form.cleaned_data['genero']
               #ver si exsite la person, si no existe agregarlo como nuevo registro
               #
               persona_data.phone = phone
               persona_data.city = city
               persona_data.region = region
               persona_data.genero = genero
               persona_data.save()
               messages.success(request,'Tus datos se han actualizado!')

        # cambia la contraseña
        if 'savePassword' in request.POST:
            print('scambiar poass')
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user) 
                messages.success(request, 'Your password was successfully updated!')
            else:
                print('here')
                messages.error(request, 'Error en cambiar la clave')
        #....
  
    else:
        user_form = UserEditForms(instance= request.user)
        password_form = PasswordChangeForm(request.user)
        

    return render(request, 
                'backoffice/profile.html',
                {'user_form':user_form,
                'password_form':password_form,
                'persona_form': persona_form,
                'fotografo_form': fotografo_form})



@login_required
def createPost(request):
  print("se llamo a create post")

  ImageFormSet = modelformset_factory(PostPicture, form=PicturesForm, extra=4)
  #'extra' means the number of photos that you can upload   ^
  print("antes del if")
  if request.method == 'POST':
    
    postForm = PostForm(request.POST)
    formset = ImageFormSet(request.POST, request.FILES, queryset=PostPicture.objects.none())
    
    if postForm.is_valid():
        post_form = postForm.save(commit=False)
        post_form.author = request.user
        post_form.save()
        if formset.is_valid():  
            for form in formset.cleaned_data:
            #this helps to not crash if the user   
            #do not upload all the photos
                if form:
                    picture = form['image']
                    print(picture)
                    photo = PostPicture(post=post_form, image=picture)
                    photo.save()
        else:
            print(formset.errors)
        print("createPost")
        messages.success(request, 'Se ha creado tu post')

    else:
      print (postForm.errors, formset.errors)
  else:
      print("else ")

      postForm = PostForm()
      formset = ImageFormSet(queryset=PostPicture.objects.none())
      print('asdf')
  return render(request, 'post/create.html',
                {'postForm': postForm, 'formset': formset})



class ListPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post/posts.html'
    ordering = ['-created_on']




class DetailPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post/detail.html'

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

class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post/edit.html'

    def get_success_url(self, **kwargs):         
        return reverse_lazy('blog:detail', args=(self.object.id,))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ImageFormSet = modelformset_factory(PostPicture, form=PicturesForm, extra=4)
        context['formset'] = ImageFormSet(queryset=PostPicture.objects.filter(post_id=self.object.id))
        return context   

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        ImageFormSet = modelformset_factory(PostPicture, form=PicturesForm, extra=4, can_delete=True)
        
        formset = ImageFormSet(request.POST, request.FILES )
          
        if formset.is_valid():  
                for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                    if form:

                        picture = form['image']

                        photo = PostPicture(post=self.object, image=picture)
                        photo.save()
        else:
                print(formset.errors)
                messages.error(request, 'Tu post no se ha editado')

        messages.success(request, 'Tu post se ha editado')
        return super(UpdatePostView, self).post(request, *args, **kwargs)

        #return reverse_lazy('blog:detail', args=(self.objec,))



class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/delete.html'
    success_url = reverse_lazy('backoffice:posts')




#error 404

class Error404view(TemplateView):
    template_name = 'backoffice/error_404.html'
