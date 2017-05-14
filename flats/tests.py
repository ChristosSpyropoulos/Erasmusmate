# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from flats.models import FlatProfile
from django.contrib.auth.models import User

import datetime


class FlatProfileTestCase(TestCase):
        def setUp(self):
            self.user = User.objects.create(username="testuser")
            self.flat = FlatProfile.objects.create(user=self.user, name="testflat")
            self.date = datetime.datetime.now()


        def test_default_values(self):
            self.assertEqual(self.user, self.flat.user)

            self.assertEqual(self.flat.name, "testflat")

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

            self.assertAlmostEqual(self.flat.date, self.date)


        def test_str(self):
            self.assertEqual(self.flat.__str__(), "Flat: testflat")
