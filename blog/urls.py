from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import PwdResetForm, PwdResetConfirmForm
from backoffice.forms import UserLoginForm
from .views import LoginFormView, terms

app_name = 'blog'

urlpatterns = [
  #path('', views.PostList.as_view(), name="index"),
  path('', views.testingIndex, name="index"),  
  path('terminosdecontrato',views.terms,name="terms"),

  path('blog', views.blogList.as_view(), name = "blog"),
  path('blog/<int:id>/', views.blogFiltred.as_view(), name="blogFiltred"),


  path('posts/<int:id>/', views.PostDetail.as_view(), name="detail"),

  #path('posts/<int:id>/', views.PostDetail.as_view(), name="detail"),
  path('testing', views.testing_website, name='testing'),
  #path('work-with-us',views.accounts_register, name="workwithus"),
  path('activate/<slug:uidb64>/<slug:token>)/', views.activate, name="activate"),
  path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'accounts/password_reset_form.html',
                                                              form_class=PwdResetForm,
                                                              email_template_name = 'accounts/password_reset_email.html'), name='pwdreset'),
  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name ='accounts/password_reset_done.html'), name='password_reset_done'),

  path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
    template_name='accounts/password_reset_confirm.html'), name= "password_reset_confirm"),

  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    template_name='accounts/password_reset_complete.html'), name= "password_reset_complete"),


  path('work-with-us', views.workwithus, name='trabajaconnosotros'),
  path('register/', views.accounts_register, name= 'register'),
  path('login/', LoginFormView.as_view(), name = 'login'),
  path('about-us',views.sobreNosotros, name = 'about-us')
]
urlpatterns = format_suffix_patterns(urlpatterns)


  #path('login/', auth_views.LoginView.as_view(template_name="registration/login.html",
  #                                            authentication_form =UserLoginForm), name='login'),
