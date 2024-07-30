from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django import forms
from .forms import StudentSignUpForm, PractitionerSignUpForm
from .decorators import student_required, practitioner_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm





from django.shortcuts import render, get_object_or_404, redirect
from .models import Assignment, Submission
from .forms import SubmissionForm
from django.contrib.auth.decorators import login_required



from django.shortcuts import render, get_object_or_404, redirect
from .models import Submission, Assignment, User
import random


User = get_user_model()

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_student:
                    return redirect('student_dashboard')
                elif user.is_staff:
                    return redirect('adminpage')
                elif user.is_practitioner:
                    return redirect('practitioner_dashboard')
            else:
                messages.error(request, "Please enter a correct username and password.")
        else:
            messages.error(request, "Please enter a correct username and password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form}) 


def student_register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'registration/student_register.html', {'form': form})

def practitioner_register(request):
    if request.method == 'POST':
        form = PractitionerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('practitioner_dashboard')
    else:
        form = PractitionerSignUpForm()
    return render(request, 'registration/practitioner_register.html', {'form': form})

def adminpage(request):
    return render(request, 'adminpage.html')


@login_required
@practitioner_required
def practitioner_dashboard(request):
    return render(request, 'practitioner_dashboard.html')

@login_required
@student_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')


def logout_user(request):
    auth_logout(request)
    return redirect('login')

# def logout_user1(request):
#     auth_logout(request)
#     return redirect('login')

# def logout_user2(request):
#     auth_logout(request)
#     return redirect('login')








class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('change_password')

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the error below.')
        return super().form_invalid(form)


# class CustomPasswordChangeView1(PasswordChangeView):
#     template_name = 'change_password.html'
#     success_url = reverse_lazy('change_password')

#     def form_valid(self, form):
#         messages.success(self.request, 'Your password was successfully updated!')
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         messages.error(self.request, 'Please correct the error below.')
#         return super().form_invalid(form)
class EmailForm(forms.Form):
    email = forms.EmailField()

class CodeVerificationForm(forms.Form):
    code = forms.CharField(max_length=4, required=True)

#similar to student
class PasswordResetRequestView(View):
    def get(self, request):
        # Clear previous session data related to password reset
        if 'reset_code' in request.session:
            del request.session['reset_code']
        if 'uidb64' in request.session:
            del request.session['uidb64']
        if 'token' in request.session:
            del request.session['token']
            
        return render(request, 'password_reset.html', {'form': EmailForm()})
    
    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset_code = str(random.randint(1000, 9999))  # Generate a 4-digit code
            request.session['reset_code'] = reset_code
            request.session['uidb64'] = urlsafe_base64_encode(force_bytes(user.pk))
            request.session['token'] = default_token_generator.make_token(user)
            send_mail(
                'Password Reset Code',
                f'Your password reset code is {reset_code}',
                'aliafawi51@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset code has been sent to your email.')
            return redirect('verify_code')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
            return render(request, 'password_reset.html', {'form': EmailForm()})
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'password_reset.html', {'form': EmailForm()})



from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    try:
        send_mail(
            'Test Email',
            'This is a test email sent from Django.',
            'aliafawi51@gmail.com',
            ['aliafawi51@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse("Test email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Failed to send email, error: {str(e)}")

class CodeVerificationView(View):
    def get(self, request):
        form = CodeVerificationForm()
        return render(request, 'verify_code.html', {'form': form})

    def post(self, request):
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == request.session.get('reset_code'):
                uidb64 = request.session.get('uidb64')
                token = request.session.get('token')
                if uidb64 and token:
                    return redirect(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
                else:
                    messages.error(request, 'Session expired or invalid. Please try again.')
                    return redirect('password_reset')
            else:
                messages.error(request, 'Invalid code. Please try again.')
                return redirect('verify_code')
        return render(request, 'verify_code.html', {'form': form})
    
    
def custom_404(request, exception=None):
    return render(request, '404.html', status=404)




@login_required
@practitioner_required
def add_recording(request):
    if request.method == 'POST':
        form = RecordingForm(request.POST, request.FILES)
        if form.is_valid():
            recording = form.save(commit=False)
            recording.uploaded_by = request.user
            recording.save()
            messages.success(request, "Recording uploaded successfully.")
            return redirect('practitioner_dashboard')
    else:
        form = RecordingForm()
    return render(request, 'add_recording.html', {'form': form})



@login_required
def exams(request):
    assignments = Assignment.objects.all()
    submissions = Submission.objects.filter(student=request.user)
    submission_dict = {submission.assignment_id: submission for submission in submissions}

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = get_object_or_404(Assignment, pk=request.POST.get('assignment_id'))
            if assignment.id not in submission_dict:
                submission = form.save(commit=False)
                submission.student = request.user
                submission.assignment = assignment
                submission.save()
            return redirect('exams')  # Redirect to the same page to display the updated data

    return render(request, 'exams.html', {
        'assignments': assignments,
        'submission_dict': submission_dict,
        'form': SubmissionForm()
    })



