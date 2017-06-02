# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from accounts.models import Profile, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import RegistrationForm

from django.core.urlresolvers import reverse
from django.utils import timezone

# Create your tests here.


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user2 = User.objects.create(username="testuser")
        self.userprofile = UserProfile.objects.create(
            user=self.user2,
            sex="male",
            university="AGH",
            country_of_origin="Greece",
            faculty="informatyka",
            user_id = 101,
            age=18,
            email = "user@email.com",
            prefered_cuisine = "CHINESE"
        )

        self.date = timezone.now()


    def test_default_values(self):
        self.assertEqual(self.user2, self.userprofile.user)
        self.assertEqual(self.userprofile.sex, "male")
        self.assertEqual(self.userprofile.country_of_origin, "Greece")
        self.assertEqual(self.userprofile.faculty, "informatyka")
        self.assertEqual(self.userprofile.age, 18)
        self.assertEqual(self.userprofile.university, "AGH")
        self.assertEqual(self.userprofile.email, "user@email.com")
        self.assertEqual(self.userprofile.phone, 0)
        self.assertEqual(self.userprofile.country_of_studies, "")
        self.assertEqual(self.userprofile.city_of_studies, "")
        self.assertEqual(self.userprofile.region, "")
        self.assertIn(self.userprofile.prefered_cuisine, dict(UserProfile.CUISINE_CHOICES))
        self.assertEqual(self.userprofile.description, "")
        self.assertIsNone(self.userprofile.image._file)
        self.assertIn(self.userprofile.hardworking, dict(UserProfile.RATE_CHOICES))
        self.assertIn(self.userprofile.partying, dict(UserProfile.RATE_CHOICES))
        self.assertIn(self.userprofile.traveling, dict(UserProfile.RATE_CHOICES))
        self.assertEqual(self.userprofile.price, 0)
        self.assertIn(self.userprofile.smoking_permitted, dict(UserProfile.RATE_CHOICES))
        self.assertIn(self.userprofile.same_nationality_roommates, dict(UserProfile.CHOICES))
        self.assertIn(self.userprofile.time_of_staying_in_flat, dict(UserProfile.TIME_CHOICES))
        self.assertIn(self.userprofile.men_or_women_on_room, dict(UserProfile.MEN_OR_WOMEN_CHOICES))
        self.assertIn(self.userprofile.num_of_roommates, dict(UserProfile.NUM_OF_PEOPLE_CHOICES))
        self.assertTrue(abs(self.userprofile.date-self.date)<timezone.timedelta(seconds=1))


    def test_str(self):
        self.assertEqual(self.userprofile.__str__(), "Profile of testuser")


class UserTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="secret")
        self.user2 = User.objects.create(username="user2")
        self.user3 = User.objects.create(username="user3")
        self.user4 = User.objects.create(username="user4")
        self.user5 = User.objects.create_user(username="user5", password="secret")

        self.userprofile1 = UserProfile.objects.create(
            user=self.user2,
            sex="male",
            university="AGH",
            country_of_origin="Greece",
            faculty="informatyka",
            user_id = 101,
            age=18,
            email = "user@email.com",
            prefered_cuisine = "CHINESE"
        )

    def test_view_profile(self):
        self.client.login(username='user1', password='secret')
        response1 = self.client.get(reverse('accounts:view_profile_with_pk', args={'2'}))
        response2 = self.client.get(reverse('accounts:view_profile_with_pk', args={'400'}))

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 404)



    def test_edit_profile(self):
        self.client.login(username='user1', password='secret')
        data = { 'age': 18,
                 'sex':"MALE",
                 'email':'geo@email.com',
                 'phone':697632343,
                 'country_of_origin':'Greece',
                 'country_of_studies':'Poland',
                 'city_of_studies':'Krakow',
                 'region':'center',
                 'university': "AGH",
                 'faculty':'informatyka',
                 'prefered_cuisine':"CHINESE",
                 'hardworking': "Don't care",
                 'partying': "Don't care",
                 'traveling': "Don't care",
                 'smoking_permitted': "Don't care",
                 'same_nationality_roommates': "Don't care",
                 'men_or_women_on_room': "Don't care",
                 'description': "nice user1",
                 'num_of_roommates':"Don't care",
                 'time_of_staying_in_flat':'UNKNOWN',
                 'price':200,
        }
        response1 = self.client.get(reverse('accounts:edit_profile'))
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.post(reverse('accounts:edit_profile'), data)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse('accounts:view_profile'))


    def test_view_list_accounts(self):
        self.client.login(username='user1', password='secret')
        response1 = self.client.get(reverse('accounts:view_list_accounts'))
        response2 = self.client.post(reverse('accounts:view_list_accounts'), {'users': UserProfile.objects.get(user=self.user2)})
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, self.user2)
        self.assertEqual(response2.status_code, 200)



    def test_change_password(self):
        self.client.login(username='user1', password='secret')
        data1 = { 'old_password': 'sdsdkld',
                 'new_password1': 'qweasdzxcv',
                 'new_password2': 'qweasdzxcv',
                 #'error_messages':'Please',
        }
        data2 = { 'old_password': 'secret',
                 'new_password1': 'qweasdzxcv',
                 'new_password2': 'qsdsdskscv',
                 #'error_messages':'Please',
        }
        data3 = { 'old_password': 'secret',
                 'new_password1': 'qweasdzxcv',
                 'new_password2': 'qweasdzxcv',
                 #'error_messages':'Please',
        }
        response1 = self.client.get(reverse('accounts:change_password'))
        response2 = self.client.post(reverse('accounts:change_password'), data1)
        response3 = self.client.post(reverse('accounts:change_password'), data2)
        response4 = self.client.post(reverse('accounts:change_password'), data3)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse('accounts:change_password'))
        self.assertEqual(response3.status_code, 302)
        self.assertRedirects(response3, reverse('accounts:change_password'))
        self.assertEqual(response4.status_code, 302)
        self.assertRedirects(response4, reverse('accounts:view_profile'))


    def test_incorrect_password(self):
        self.client.login(username='user1', password='secret')
        data = {
            'old_password': 'test',
            'new_password1': 'abc123',
            'new_password2': 'abc123',
            }
        form = PasswordChangeForm(self.user1, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["old_password"].errors,
                         [u'Your old password was entered incorrectly. Please enter it again.'])


    def test_password_verification(self):
        # The two new passwords do not match.
        self.client.login(username='user1', password='secret')
        data = {
            'old_password': 'password',
            'new_password1': 'abc123',
            'new_password2': 'abc',
            }
        form = PasswordChangeForm(self.user1, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["new_password2"].errors,
                         [u"The two password fields didn't match."])


    '''def test_success(self):
        # The success case.
        self.client.login(username='user1', password='secret')
        #user = User.objects.get(username='testclient')
        data = {
            'old_password': 'password',
            'new_password1': 'abc123qqqq',
            'new_password2': 'abc123qqqq',
            }
        form = PasswordChangeForm(self.user1, data)
        self.assertTrue(form.is_valid())'''

    def test_field_order(self):
        # Regression test - check the order of fields:
        self.client.login(username='user1', password='secret')
        self.assertEqual(PasswordChangeForm(self.user1, {}).fields.keys(),
                         ['old_password', 'new_password1', 'new_password2'])


    def test_register(self):
        data = { 'username':'Team',
                 'first_name':'Teamname',
                 'last_name':'TeamSurname',
                 'email':'teamemail@email.com',
                 'password1':'qweasdzxc',
                 'password2':'qweasdzxc',
        }
        response1 = self.client.get(reverse('accounts:register'))
        response2 = self.client.post(reverse('accounts:register'), data)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse('home:home'))
