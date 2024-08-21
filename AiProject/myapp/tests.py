from django.test import TestCase
from .models import User, Student, Practitioner, Recording, StudyMaterial, Assignment, Submission, Favorite

class ModelsTest(TestCase):

    def setUp(self):
        self.user_student = User.objects.create_user(username='student1', email='student1@example.com', password='password123')
        self.user_practitioner = User.objects.create_user(username='practitioner1', email='practitioner1@example.com', password='password123')

    def test_student_creation(self):
        student = Student.objects.create(user=self.user_student)
        self.assertEqual(student.user.username, 'student1')

    def test_practitioner_creation(self):
        practitioner = Practitioner.objects.create(user=self.user_practitioner)
        self.assertEqual(practitioner.user.username, 'practitioner1')

    def test_recording_creation(self):
        recording = Recording.objects.create(
            title='Lecture 1',
            description='Introduction to Django',
            uploaded_by=self.user_practitioner
        )
        self.assertEqual(str(recording), 'Lecture 1')

    def test_study_material_creation(self):
        study_material = StudyMaterial.objects.create(
            title='Study Material 1',
            description='Chapter 1 Notes',
            uploaded_by=self.user_practitioner
        )
        self.assertEqual(str(study_material), 'Study Material 1')

    def test_assignment_creation(self):
        assignment = Assignment.objects.create(
            title='Assignment 1',
            description='Solve the problems in the attached file.',
            practitioner=self.user_practitioner
        )
        self.assertEqual(str(assignment), 'Assignment 1')

    def test_submission_creation(self):
        assignment = Assignment.objects.create(
            title='Assignment 1',
            description='Solve the problems in the attached file.',
            practitioner=self.user_practitioner
        )
        submission = Submission.objects.create(
            assignment=assignment,
            student=self.user_student,
            grade='100'
        )
        self.assertEqual(str(submission), 'Submission by student1 for Assignment 1')

    def test_favorite_creation(self):
        recording = Recording.objects.create(
            title='Lecture 1',
            description='Introduction to Django',
            uploaded_by=self.user_practitioner
        )
        favorite = Favorite.objects.create(user=self.user_student, recording=recording)
        self.assertEqual(str(favorite), 'student1 - Lecture 1')






from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import User, Recording, Assignment, Submission

class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_student = User.objects.create_user(username='student1', email='student1@example.com', password='password123')
        self.user_practitioner = User.objects.create_user(username='practitioner1', email='practitioner1@example.com', password='password123')

    def test_student_register_view(self):
        response = self.client.get(reverse('student_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/student_register.html')

    def test_practitioner_register_view(self):
        response = self.client.get(reverse('practitioner_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/practitioner_register.html')

    def test_add_recording_view(self):
        self.client.login(username='practitioner1', password='password123')
        response = self.client.get(reverse('add_recording'))


    def test_add_study_material_view(self):
        self.client.login(username='practitioner1', password='password123')
        response = self.client.get(reverse('add_study_material'))


    def test_exams_view(self):
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('exams'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exams.html')

    def test_my_courses_view(self):
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('myCourses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myCourses.html')

    def test_toggle_favorite_view(self):
        self.client.login(username='student1', password='password123')
        recording = Recording.objects.create(
            title='Lecture 1',
            description='Introduction to Django',
            uploaded_by=self.user_practitioner
        )
        response = self.client.post(reverse('toggle_favorite', args=[recording.id]))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, '{"status":"added"}')








import random
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from myapp.models import Recording, Favorite
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import outbox
from myapp.models import Assignment, Submission
from django.core.files.uploadedfile import SimpleUploadedFile


from django.test import TestCase
from .forms import StudentSignUpForm, PractitionerSignUpForm, RecordingForm, StudyMaterialForm, AssignmentForm, SubmissionForm
from .models import User, Recording, StudyMaterial, Assignment, Submission

class FormsTest(TestCase):

    def test_student_signup_form_valid(self):
        form_data = {
            'username': 'student1',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'student1@example.com',
            'password1': 'mmllmkmm',
            'password2': 'mmllmkmm'
        }
        form = StudentSignUpForm(data=form_data)
        if not form.is_valid():
            print(form.errors)  # Add this line to see why the form is failing
        self.assertTrue(form.is_valid())

    def test_practitioner_signup_form_valid(self):
        form_data = {
            'username': 'practitioner1',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'practitioner1@example.com',
            'password1': 'mmllmkmm',
            'password2': 'mmllmkmm'
        }
        form = PractitionerSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())


User = get_user_model()

class UserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(
            username='studentuser', password='ComplexPass123!', email='student@example.com', is_student=True
        )
        self.practitioner = User.objects.create_user(
            username='practitioneruser', password='ComplexPass123!', email='practitioner@example.com', is_practitioner=True
        )

    def test_login_student(self):
        response = self.client.post(reverse('login'), {'username': 'studentuser', 'password': 'ComplexPass123!'})
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_login_practitioner(self):
        response = self.client.post(reverse('login'), {'username': 'practitioneruser', 'password': 'ComplexPass123!'})
        self.assertRedirects(response, reverse('practitioner_dashboard'))

    def test_student_register(self):
        response = self.client.post(reverse('student_register'), {
            'username': 'newstudent',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newstudent@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertEqual(response.status_code, 302)  # Ensure it redirects
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_practitioner_register(self):
        response = self.client.post(reverse('practitioner_register'), {
            'username': 'newpractitioner',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'newpractitioner@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertEqual(response.status_code, 302)  # Ensure it redirects
        self.assertRedirects(response, reverse('practitioner_dashboard'))

    def test_password_reset(self):
        response = self.client.post(reverse('password_reset'), {'email': 'student@example.com'})
        self.assertEqual(response.status_code, 302)  # Ensure it redirects
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Your password reset code is', mail.outbox[0].body)  # Check the email body content

    def test_404_page(self):
        response = self.client.get('/nonexistentpage/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_logout(self):
        self.client.login(username='studentuser', password='ComplexPass123!')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

class ChangePasswordTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='old_password123', email='testuser@example.com'
        )
        self.client.login(username='testuser', password='old_password123')

    def test_change_password(self):
        response = self.client.post(reverse('change_password'), {
            'old_password': 'old_password123',
            'new_password1': 'new_secure_password123',
            'new_password2': 'new_secure_password123',
        })
        self.assertRedirects(response, reverse('change_password'))

        # Ensure the password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_secure_password123'))

        # Check if a success message is in the response
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your password was successfully updated!')




User = get_user_model()
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import outbox
from django.core.files.uploadedfile import SimpleUploadedFile
from myapp.models import Assignment, Submission

User = get_user_model()

class MyAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(
            username='studentuser', password='ComplexPass123!', email='student@example.com', is_student=True
        )
        self.practitioner = User.objects.create_user(
            username='practitioneruser', password='ComplexPass123!', email='practitioner@example.com', is_practitioner=True
        )
        self.client.login(username='practitioneruser', password='ComplexPass123!')
        self.assignment = Assignment.objects.create(
            title='Test Assignment', description='Test Description', practitioner=self.practitioner
        )
        self.submission = Submission.objects.create(
            assignment=self.assignment, student=self.student, grade='B', notes='Needs improvement',
            file=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")
        )



    def test_students_grade_view_post(self):
        response = self.client.post(reverse('studentsGrade'), {
            'grade': '100',
            'notes': 'Excellent work',
            'submission_id': self.submission.id
        })
        self.assertEqual(response.status_code, 302)  # Ensure it redirects
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.grade, '100')
        self.assertEqual(self.submission.notes, 'Excellent work')

    def test_grades_view(self):
        self.client.login(username='studentuser', password='ComplexPass123!')
        response = self.client.get(reverse('grades'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grades.html')
        self.assertContains(response, self.assignment.title)
        self.assertContains(response, self.submission.grade)





from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from myapp.models import Recording, Favorite

User = get_user_model()

class FavoriteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create a sample file
        self.sample_file = SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")

        self.recording = Recording.objects.create(
            title='Test Recording',
            description='Test Description',
            confession=self.sample_file,
            uploaded_by=self.user
        )

    def test_toggle_favorite_add(self):
        response = self.client.post(reverse('toggle_favorite', args=[self.recording.id]), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'added'})

        favorite_exists = Favorite.objects.filter(user=self.user, recording=self.recording).exists()
        self.assertTrue(favorite_exists)

    def test_toggle_favorite_remove(self):
        Favorite.objects.create(user=self.user, recording=self.recording)
        response = self.client.post(reverse('toggle_favorite', args=[self.recording.id]), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'removed'})

        favorite_exists = Favorite.objects.filter(user=self.user, recording=self.recording).exists()
        self.assertFalse(favorite_exists)

    def test_my_favorites(self):
        Favorite.objects.create(user=self.user, recording=self.recording)
        response = self.client.get(reverse('my_favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_favorites.html')
        self.assertContains(response, self.recording.title)



from django.test import TestCase
from .models import User, Student, Practitioner, Recording, StudyMaterial, Assignment, Submission, Favorite

class ModelsTest(TestCase):

    def setUp(self):
        self.user_student = User.objects.create_user(username='student1', email='student1@example.com', password='password123')
        self.user_practitioner = User.objects.create_user(username='practitioner1', email='practitioner1@example.com', password='password123')

    def test_student_creation(self):
        student = Student.objects.create(user=self.user_student)
        self.assertEqual(student.user.username, 'student1')

    def test_practitioner_creation(self):
        practitioner = Practitioner.objects.create(user=self.user_practitioner)
        self.assertEqual(practitioner.user.username, 'practitioner1')

    def test_recording_creation(self):
        recording = Recording.objects.create(
            title='Lecture 1',
            description='Introduction to Django',
            uploaded_by=self.user_practitioner
        )
        self.assertEqual(str(recording), 'Lecture 1')

    def test_study_material_creation(self):
        study_material = StudyMaterial.objects.create(
            title='Study Material 1',
            description='Chapter 1 Notes',
            uploaded_by=self.user_practitioner
        )
        self.assertEqual(str(study_material), 'Study Material 1')

    def test_assignment_creation(self):
        assignment = Assignment.objects.create(
            title='Assignment 1',
            description='Solve the problems in the attached file.',
            practitioner=self.user_practitioner
        )
        self.assertEqual(str(assignment), 'Assignment 1')

    def test_submission_creation(self):
        assignment = Assignment.objects.create(
            title='Assignment 1',
            description='Solve the problems in the attached file.',
            practitioner=self.user_practitioner
        )
        submission = Submission.objects.create(
            assignment=assignment,
            student=self.user_student,
            grade='100'
        )
        self.assertEqual(str(submission), 'Submission by student1 for Assignment 1')

    def test_favorite_creation(self):
        recording = Recording.objects.create(
            title='Lecture 1',
            description='Introduction to Django',
            uploaded_by=self.user_practitioner
        )
        favorite = Favorite.objects.create(user=self.user_student, recording=recording)
        self.assertEqual(str(favorite), 'student1 - Lecture 1')






from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import User, Recording, Assignment, Submission

class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_student = User.objects.create_user(username='student1', email='student1@example.com', password='password123')
        self.user_practitioner = User.objects.create_user(username='practitioner1', email='practitioner1@example.com', password='password123')

    def test_student_register_view(self):
        response = self.client.get(reverse('student_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/student_register.html')

    def test_practitioner_register_view(self):
        response = self.client.get(reverse('practitioner_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/practitioner_register.html')

    def test_add_recording_view(self):
        self.client.login(username='practitioner1', password='password123')
        response = self.client.get(reverse('add_recording'))


    def test_add_study_material_view(self):
        self.client.login(username='practitioner1', password='password123')
        response = self.client.get(reverse('add_study_material'))


    def test_exams_view(self):
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('exams'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exams.html')

    def test_my_courses_view(self):
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('myCourses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myCourses.html')

    def test_toggle_favorite_view(self):
        self.client.login(username='student1', password='password123')
        recording = Recording.objects.create(
            title='Lecture 1',
            description='Introduction to Django',
            uploaded_by=self.user_practitioner
        )
        response = self.client.post(reverse('toggle_favorite', args=[recording.id]))
        self.assertEqual(response.status_code, 200)





from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from myapp.models import Recording, Assignment, Submission, Favorite

User = get_user_model()

class URLTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username='studentuser', password='password123', email='student@example.com', is_student=True)
        self.practitioner = User.objects.create_user(username='practitioneruser', password='password123', email='practitioner@example.com', is_practitioner=True)
        self.admin_user = User.objects.create_superuser(username='adminuser', password='password123', email='admin@example.com')

    def test_admin_url(self):
        self.client.login(username='adminuser', password='password123')
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
       
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_student_dashboard_url(self):
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')

    def test_practitioner_dashboard_url(self):
        self.client.login(username='practitioneruser', password='password123')
        response = self.client.get(reverse('practitioner_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'practitioner_dashboard.html')

    def test_adminpage_url(self):
        self.client.login(username='adminuser', password='password123')
        response = self.client.get(reverse('adminpage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminpage.html')

    def test_add_recording_url(self):
        self.client.login(username='practitioneruser', password='password123')
        response = self.client.get(reverse('add_recording'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_recording.html')

    def test_add_study_material_url(self):
        self.client.login(username='practitioneruser', password='password123')
        response = self.client.get(reverse('add_study_material'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_study_material.html')

    def test_new_test_url(self):
        self.client.login(username='practitioneruser', password='password123')
        response = self.client.get(reverse('newTest'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newTest.html')

    def test_students_grade_url(self):
        self.client.login(username='practitioneruser', password='password123')
        response = self.client.get(reverse('studentsGrade'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studentsGrade.html')

    def test_my_courses_url(self):
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('myCourses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myCourses.html')

    def test_files_url(self):
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('files'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files.html')

    def test_grades_url(self):
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('grades'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grades.html')

    def test_exams_url(self):
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('exams'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exams.html')

    def test_logout_url(self):
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login after logout

    def test_password_reset_url(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset.html')

    def test_verify_code_url(self):
        response = self.client.get(reverse('verify_code'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'verify_code.html')

    def test_toggle_favorite_url(self):
        self.client.login(username='studentuser', password='password123')
        recording = Recording.objects.create(title='Test Recording', uploaded_by=self.practitioner)
        response = self.client.post(reverse('toggle_favorite', args=[recording.id]))
        self.assertEqual(response.status_code, 200)

    def test_my_favorites_url(self):
        self.client.login(username='studentuser', password='password123')
        response = self.client.get(reverse('my_favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_favorites.html')

    def test_delete_user_url(self):
        self.client.login(username='adminuser', password='password123')
        response = self.client.post(reverse('delete_user', args=[self.student.username]))
        self.assertEqual(response.status_code, 200)

    def test_delete_recording_url(self):
        self.client.login(username='adminuser', password='password123')
        recording = Recording.objects.create(title='Test Recording', uploaded_by=self.practitioner)
        response = self.client.post(reverse('delete_recording', args=[recording.id]))
        self.assertEqual(response.status_code, 200)

    def test_custom_404(self):
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')