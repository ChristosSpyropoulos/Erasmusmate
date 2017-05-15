# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from flats.models import FlatProfile
from django.contrib.auth.models import User

from django.utils import timezone


class FlatProfileTestCase(TestCase):
        def setUp(self):
            self.user = User.objects.create(username="testuser")
            self.flat = FlatProfile.objects.create(
                            user=self.user,
                            name="testflat",
                            place="AGH",
                            price=500,
                            time_of_staying_in_flat="1 MONTH",
                            num_of_people_total="2",
                            num_of_people_available="1"
                        )
            self.date = timezone.now()


        def test_default_values(self):
            self.assertEqual(self.user, self.flat.user)

            self.assertEqual(self.flat.name, "testflat")

            self.assertEqual(self.flat.description, "")

            self.assertIn(self.flat.place, dict(FlatProfile.PLACE_CHOICES))

            self.assertEqual(self.flat.adress, "")

            self.assertEqual(self.flat.price, 500)

            self.assertEqual(self.flat.smoker, "Don't care")

            self.assertEqual(self.flat.same_nationality_roommates, "Don't care")

            self.assertIn(self.flat.time_of_staying_in_flat, dict(FlatProfile.TIME_CHOICES))

            self.assertIn(self.flat.num_of_people_total, dict(FlatProfile.NUM_OF_PEOPLE_CHOICES))

            self.assertIn(self.flat.num_of_people_available, dict(FlatProfile.NUM_OF_PEOPLE_CHOICES))

            self.assertEqual(self.flat.men_or_women_on_room, "Don't care")

            self.assertEqual(self.flat.couples_accepted, "Don't care")

            self.assertIsNone(self.flat.image._file)

            self.assertTrue(abs(self.flat.date-self.date)<timezone.timedelta(seconds=1))


        def test_str(self):
            self.assertEqual(self.flat.__str__(), "Flat: testflat")
