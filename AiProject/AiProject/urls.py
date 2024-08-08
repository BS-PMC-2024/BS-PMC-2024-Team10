from django.conf.urls import handler404
from django.urls import path # type: ignore
from myapp import views
from django.contrib import admin # type: ignore
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import delete_user
from myapp import views
from myapp.views import myCourses, toggle_favorite, my_favorites

urlpatterns = [
    # admin 

    path('',views.custom_login, name='login'),
    path('admin/', admin.site.urls),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('adminpage/users', views.users, name='users'),
    path('adminpage/report', views.report, name='report'),


    #student

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student_dashboard/myCourses/', views.myCourses, name='myCourses'),
    path('student_dashboard/exams/',views.exams, name='exams'),
    path('student_dashboard/files/', views.files, name='files'),
    path('student_dashboard/grades/',views.grades, name='grades'),
    path('student_register/', views.student_register, name='student_register'),

    # practitioner
    path('practitioner_dashboard/', views.practitioner_dashboard, name='practitioner_dashboard'),
    path('practitioner_dashboard/add_recording/',views.add_recording, name='add_recording'),
    path('practitioner_register/', views.practitioner_register, name='practitioner_register'),
    path('practitioner_dashboard/Courses/',views.Courses, name='Courses'),
    path('practitioner_dashboard/newTest/',views.newTest, name='newTest'),
    path('practitioner_dashboard/studentsGrade/',views.studentsGrade, name='studentsGrade'),


    # for all
    path('logout/', views.logout_user, name='logout'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('verify_code/', views.CodeVerificationView.as_view(), name='verify_code'),
    path('add_study_material/', views.add_study_material, name='add_study_material'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),



    path('toggle_favorite/<int:recording_id>/', toggle_favorite, name='toggle_favorite'),
    path('my_favorites/', my_favorites, name='my_favorites'),
   
]
handler404 = 'myapp.views.custom_404'