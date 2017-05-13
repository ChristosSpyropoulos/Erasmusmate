# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from flats.models import FlatProfile
from django.contrib.auth.models import User

class FlatProfileTestCase(TestCase):
        def SetUp(self):
            user = User.objects.create(username="testuser")
            flat = FlatProfile.objects.create(user=user)

        def test_default_values(self):
            self.assertEqual(user, self.flat.user)

            self.assertIsNotNone(self.flat.name)
            self.assertTrue(len(self.flat.name)>1)

            self.assertIsNone(self.flat.description)

            self.assertIn(self.flat.place, FlatProfile.PLACE_CHOICES)

            self.assertIsNone(self.flat.adress)

            self.assertIsNone(self.flat.price)

            self.assertEqual(self.flat.smoker, "Don't care")

            self.assertEqual(self.flat.same_nationality_roomates, "Don't care")

            self.assertIn(self.flat.time_of_staying_in_flat, FlatProfile.TIME_CHOICES)

            self.assertIn(self.flat.num_of_people_total, FlatProfile.NUM_OF_PEOPLE_CHOICES)

            self.assertIn(self.flat.num_of_people_available, FlatProfile.NUM_OF_PEOPLE_CHOICES)

            self.assertEqual(self.flat.men_or_women_on_room, "Don't care")

            self.asserEqual(self.flat.couples_accepted, "Don't care")

            self.assertIsNone(self.flat.image)
            
