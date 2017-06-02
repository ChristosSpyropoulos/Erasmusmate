# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import UserProfile
from flats.models import FlatProfile
from django.core.urlresolvers import reverse
from django.conf import settings

class HomeTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.user3 = User.objects.create(username="user3")
        self.user4 = User.objects.create_user(username="user4", password="secret")
        self.user5 = User.objects.create(username="user5")
        self.user6 = User.objects.create(username="user6")
        self.user7 = User.objects.create_user(username="user7", password="secret")

        self.flat1 = FlatProfile.objects.create(user=self.user1)
        self.flat2 = FlatProfile.objects.create(user=self.user2)
        self.flat3 = FlatProfile.objects.create(user=self.user3)
        self.flat4 = FlatProfile.objects.create(user=self.user4)
        self.flat5 = FlatProfile.objects.create(user=self.user5)
        self.flat6 = FlatProfile.objects.create(user=self.user6)
        self.flat7 = FlatProfile.objects.create(user=self.user7)

    def test_middleware_login(self):
        response1 = self.client.get(reverse('home:home'))
        self.assertEqual(response1.status_code, 302)
        self.assertRedirects(response1, settings.LOGIN_URL)

        data = {
            'username': 'user7',
            'password': 'secret',
        }
        response2 = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, settings.LOGIN_REDIRECT_URL)

        response3 = self.client.get(reverse('accounts:register'))
        self.assertEqual(response3.status_code, 302)
        self.assertRedirects(response3, settings.LOGIN_REDIRECT_URL)

    def test_view_home(self):
        self.client.login(username='user7', password='secret')
        response1 = self.client.get(reverse('home:home'))

        self.assertEqual(response1.status_code, 200)

        self.assertContains(response1, self.flat7.name)
        self.assertContains(response1, self.flat6.name)
        self.assertContains(response1, self.flat5.name)
        self.assertContains(response1, self.flat4.name)
        self.assertContains(response1, self.flat3.name)

        self.assertNotContains(response1, self.user7.username)
        self.assertContains(response1, self.user6.username)
        self.assertContains(response1, self.user5.username)
        self.assertContains(response1, self.user4.username)
        self.assertContains(response1, self.user3.username)
        self.assertContains(response1, self.user2.username)

        self.client.logout()
        self.client.login(username='user4', password='secret')
        response2 = self.client.get(reverse('home:home'))
        self.assertContains(response2, self.user7.username)
        self.assertContains(response2, self.user6.username)
        self.assertContains(response2, self.user5.username)
        self.assertNotContains(response2, self.user4.username)
        self.assertContains(response2, self.user3.username)
        self.assertContains(response2, self.user2.username)
