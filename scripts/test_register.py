from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from portal.forms import CustomUserCreationForm # Import your custom form

# Get the CustomUser model defined by AUTH_USER_MODEL
CustomUser = get_user_model()

class RegistrationTests(TestCase):
    """
    Tests for the user registration view and form logic.
    """
    def setUp(self):
        """Set up client and the registration URL."""
        self.client = Client()
        self.register_url = reverse('register') # Assumes URL name is 'register'
        
        # Base data for a successful registration
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password_1': 'StrongP@ss123',
            'password_2': 'StrongP@ss123',
        }

    def test_register_page_loads_correctly(self):
        """Test that the registration page responds with 200 OK."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_successful_registration(self):
        """Test user creation and login after valid form submission."""
        
        # 1. Post the form data
        response = self.client.post(self.register_url, self.valid_data, follow=True)
        
        # 2. Check for successful creation and login
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().username, 'newuser')
        
        # 3. Check redirect to the dashboard (LOGIN_REDIRECT_URL)
        # Assumes 'dashboard' is the correct URL name
        self.assertRedirects(response, reverse('dashboard'))
        self.assertContains(response, "Account created and logged in successfully!") # Check message

    def test_registration_with_existing_username(self):
        """Test failure when attempting to register with an existing username."""
        # Create the initial user
        CustomUser.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='Password123'
        )
        
        # Data that uses the existing username
        data = {
            'username': 'testuser',
            'email': 'different@example.com',
            'password_1': 'AnotherPass456',
            'password_2': 'AnotherPass456',
        }

        # Post the duplicate data
        response = self.client.post(self.register_url, data)
        
        # Check that:
        self.assertEqual(response.status_code, 200)  # Should render the same page
        self.assertEqual(CustomUser.objects.count(), 1)  # No new user created
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

    def test_registration_password_mismatch(self):
        """Test failure when password and confirmation password do not match."""
        data = self.valid_data.copy()
        data['password_2'] = 'MISMATCHED_PASSWORD'
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertFormError(response, 'form', 'password_2', 'The two password fields didn\'t match.')

    def test_registration_email_required(self):
        """Test failure when the email field is missing (if required by your form)."""
        
        # NOTE: If your CustomUser model requires email, Django's UserCreationForm
        # needs to be customized to enforce this. Assuming your CustomUserCreationForm
        # handles email validation, this test checks for its presence.
        
        data = self.valid_data.copy()
        data['email'] = '' # Empty email
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, 200)
        # Check for error in the email field
        self.assertFormError(response, 'form', 'email', 'This field is required.')

    # Example of a test to ensure sensitive data is not logged in debug mode
    def test_passwords_not_in_context(self):
        """Ensure passwords are never present in the response context."""
        response = self.client.post(self.register_url, self.valid_data)
        
        self.assertNotIn('password_1', response.content.decode())
        self.assertNotIn('StrongP@ss123', response.content.decode())
        
        
# To run these tests, ensure your virtual environment is active and run:
# python manage.py test portal