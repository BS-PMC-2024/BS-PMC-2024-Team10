from django.conf.urls import handler404
from django.urls import path
from myapp import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('',views.custom_login, name='login'),

 path('admin/', admin.site.urls),
 path('adminpage/', views.adminpage, name='adminpage'),
    path('logout/', views.logout_user, name='logout'),
    path('student_register/', views.student_register, name='student_register'),
    path('practitioner_register/', views.practitioner_register, name='practitioner_register'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('verify_code/', views.CodeVerificationView.as_view(), name='verify_code'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]