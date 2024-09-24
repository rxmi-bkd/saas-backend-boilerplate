from rest_framework import status
from rest_framework.reverse import reverse
from shared.serializers import UserSerializer
from rest_framework.test import APIClient, APITestCase


class SessionAuthTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient(enforce_csrf_checks=True)

        cls.test_user = {'email': 'test@test.com', 'password': 'testtest', 'first_name': 'test_fn',
                         'last_name': 'test_ln'}

        serializer = UserSerializer(data=cls.test_user)
        serializer.is_valid()
        serializer.save()


class RegistrationTests(SessionAuthTests):
    def test_successful_registration(self):
        # Register
        payload = {'email': 'user@user.com', 'password': 'useruser', 'first_name': 'user_fn', 'last_name': 'user_ln'}
        response = self.client.post(reverse('session_register'), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try to log in with the fresh created account
        payload = {'email': 'user@user.com', 'password': 'useruser'}
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_with_missing_fields(self):
        response = self.client.post(reverse('session_register'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_invalid_fields(self):
        payload = {
            'email': 'bad email',
            'password': 'short',
            'first_name': 'hahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahaha',
            'last_name': 'hahahahahahahahahahahahahahahahahahahahahahahahahahahahahahahaha'
        }

        response = self.client.post(reverse('session_register'), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_existing_email(self):
        payload = {'email': 'test@test.com', 'password': 'testtest', 'first_name': 'test_fn', 'last_name': 'test_ln'}
        response = self.client.post(reverse('session_register'), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticationTests(SessionAuthTests):
    def test_successful_login(self):
        payload = {'email': 'test@test.com', 'password': 'testtest', }
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_missing_fields(self):
        response = self.client.post(reverse('session_login'), {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_invalid_credentials(self):
        payload = {'email': 'inexistant@inexistant.com', 'password': 'inexistant'}
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_successful_logout(self):
        # Log in
        payload = {'email': 'test@test.com', 'password': 'testtest', }
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Log out the account
        response = self.client.post(reverse('session_logout'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_with_unauthenticated_user(self):
        response = self.client.post(reverse('session_logout'))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserUpdateTests(SessionAuthTests):
    def test_successful_password_update(self):
        # Log in with the test account
        payload = {'email': 'test@test.com', 'password': 'testtest', }
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update the password
        payload = {'password': 'newpassword'}
        response = self.client.put(reverse('session_update_password'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Log in with the new password
        payload = {'email': 'test@test.com', 'password': 'newpassword'}
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_update_with_missing_fields(self):
        # Log in with the test account
        payload = {'email': 'test@test.com', 'password': 'testtest', }
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update the password with missing fields
        response = self.client.put(reverse('session_update_password'), {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_update_with_unauthenticated_user(self):
        response = self.client.put(reverse('session_update_password'), {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_password_update_with_invalid_password(self):
        # Log in with the test account
        payload = {'email': 'test@test.com', 'password': 'testtest', }
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update the password with invalid password
        response = self.client.put(reverse('session_update_password'), {'password': 'short'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_user_update(self):
        # Log in with the test account
        payload = {'email': 'test@test.com', 'password': 'testtest', }
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update the user
        payload = {'first_name': 'new_fn', 'last_name': 'new_ln', 'email': 'new@new.com'}
        response = self.client.put(reverse('session_update_user'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Log in with the new email
        payload = {'email': 'new@new.com', 'password': 'testtest'}
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_with_missing_fields(self):
        # Log in with the test account
        payload = {'email': 'test@test.com', 'password': 'testtest', }
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update the user with missing fields
        response = self.client.put(reverse('session_update_user'), {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_update_with_unauthenticated_user(self):
        response = self.client.put(reverse('session_update_user'), {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_with_invalid_email(self):
        # Log in with the test account
        payload = {'email': 'test@test.com', 'password': 'testtest', }
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update the user with invalid email
        payload = {'email': 'invalid email', 'first_name': 'new_fn', 'last_name': 'new_ln'}
        response = self.client.put(reverse('session_update_user'), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_update_with_existing_email(self):
        # Register a new user
        existing_user_payload = {
            'email': 'existing@test.com',
            'password': 'existingpass',
            'first_name': 'existing_fn',
            'last_name': 'existing_ln'
        }

        response = self.client.post(reverse('session_register'), existing_user_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Log in with the test account
        payload = {'email': 'test@test.com', 'password': 'testtest', }
        response = self.client.post(reverse('session_login'), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update the user with existing email
        payload = {'email': 'existing@test.com', 'first_name': 'new_fn', 'last_name': 'new_ln'}
        response = self.client.put(reverse('session_update_user'), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
