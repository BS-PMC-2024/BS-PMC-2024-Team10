import random
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

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