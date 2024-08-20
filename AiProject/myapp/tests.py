
import random
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from myapp.models import Recording, Favorite

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




from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import outbox
from myapp.models import Assignment, Submission
from django.core.files.uploadedfile import SimpleUploadedFile

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

    def test_students_grade_view_get(self):
        response = self.client.get(reverse('studentsGrade'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studentsGrade.html')
        self.assertContains(response, self.assignment.title)

    def test_students_grade_view_post(self):
        response = self.client.post(reverse('studentsGrade'), {
            'grade': 'A',
            'notes': 'Excellent work',
            'submission_id': self.submission.id
        })
        self.assertEqual(response.status_code, 302)  # Ensure it redirects
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.grade, 'A')
        self.assertEqual(self.submission.notes, 'Excellent work')
        
        # Check if an email was sent
        self.assertEqual(len(outbox), 1)
        self.assertIn('Your grade is A. Notes: Excellent work', outbox[0].body)

    def test_grades_view(self):
        self.client.login(username='studentuser', password='ComplexPass123!')
        response = self.client.get(reverse('grades'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grades.html')
        self.assertContains(response, self.assignment.title)
        self.assertContains(response, self.submission.grade)




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
        self.assertContains(response, '{"status":"added"}')

        favorite_exists = Favorite.objects.filter(user=self.user, recording=self.recording).exists()
        self.assertTrue(favorite_exists)

    def test_toggle_favorite_remove(self):
        Favorite.objects.create(user=self.user, recording=self.recording)
        response = self.client.post(reverse('toggle_favorite', args=[self.recording.id]), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '{"status":"removed"}')

        favorite_exists = Favorite.objects.filter(user=self.user, recording=self.recording).exists()
        self.assertFalse(favorite_exists)

    def test_my_favorites(self):
        Favorite.objects.create(user=self.user, recording=self.recording)
        response = self.client.get(reverse('my_favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_favorites.html')
        self.assertContains(response, self.recording.title)