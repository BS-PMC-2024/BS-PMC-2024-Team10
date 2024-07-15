

from django.conf.urls import handler404
from django.urls import path
from myapp import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
]

handler404 = 'myapp.views.custom_404'
