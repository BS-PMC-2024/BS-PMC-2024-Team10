from django.conf.urls import handler404
from django.urls import path
from myapp import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
 path('admin/', admin.site.urls),
    path('practitioner_register/', views.practitioner_register, name='practitioner_register'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
]