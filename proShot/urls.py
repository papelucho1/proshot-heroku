"""proShot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#
from django.conf.urls import handler400, handler404, handler500
#
from blog.views import Error404view, Error505view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("blog.urls")),
    path('',include('django.contrib.auth.urls')), 
    path('backoffice/',include("backoffice.urls")), 
    path('backoffice/test/',include("testProshot.urls")), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = Error404view.as_view()
handler500 = Error505view.as_error_view()