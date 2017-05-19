# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from accounts.models import Profile, UserProfile
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.utils import timezone

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.profile = Profile.objects.create(user=self.user)
        self.date = timezone.now()

    def test_default_value(self):
        self.assertEqual(self.profile.user, self.user)

        self.assertEqual(self.profile.description, "")
        self.assertIsNone(self.profile.image._file)
        self.assertTrue(abs(self.profile.date-self.date)<timezone.timedelta(seconds=1))

        self.assertEqual(self.profile.hardworking, "Don't care")
        self.assertEqual(self.profile.partying, "Don't care")
        self.assertEqual(self.profile.traveling, "Don't care")

        self.assertEqual(self.profile.price, 0)
        self.assertEqual(self.profile.smoking_permitted, "Don't care")
        self.assertEqual(self.profile.same_nationality_roommates, "Don't care")
        self.assertEqual(self.profile.time_of_staying_in_flat, "UNKNOWN")
        self.assertEqual(self.profile.men_or_women_on_room, "Don't care")
        self.assertEqual(self.profile.num_of_roommates, "Don't care")

class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
