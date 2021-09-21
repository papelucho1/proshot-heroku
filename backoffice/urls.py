from django.urls import path, include
from backoffice import views
from .views import ListPostsView, DetailPostView,  UpdatePostView, DeletePostView, usuariosViews
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, PwdChangeForm


app_name = 'backoffice'

urlpatterns = [
  path('', views.index, name= 'backoffice'),
  path('profile',views.profile, name= 'profile'),
  path('usuarios', usuariosViews.as_view(), name= 'usuarios'),
  #path('logout',views.logout_view, name='logout'),
  path('posts/',ListPostsView.as_view(), name='posts'),
  #path('posts/<int:pk>',DetailPostView.as_view(), name='detail_post'),
  path('posts/create',views.createPost, name='create_post'),
  # path('posts/create',CreatePostView.as_view(), name='create_post'),
  path('posts/edit/<int:pk>',UpdatePostView.as_view(), name='update_post'),
  path('posts/delete/<int:pk>', DeletePostView.as_view(), name='delete_post'),

 
  path('not_ready', views.not_ready, name= 'not_ready'),


 
                            
]