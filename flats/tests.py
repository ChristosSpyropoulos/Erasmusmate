# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from flats.models import FlatProfile
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
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

class FlatsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="secret")
        self.user2 = User.objects.create(username="user2")
        self.user3 = User.objects.create(username="user3")
        self.user4 = User.objects.create(username="user4")
        self.user5 = User.objects.create_user(username="user5", password="secret")

        self.flat1 = FlatProfile.objects.create(
                        user=self.user1,
                        name="flat1",
                        place="AGH",
                        price=500,
                        time_of_staying_in_flat="1 MONTH",
                        num_of_people_total="2",
                        num_of_people_available="1"
                    )
        self.flat2 = FlatProfile.objects.create(
                        user=self.user2,
                        name="flat2",
                        place="AGH",
                        price=500,
                        time_of_staying_in_flat="1 MONTH",
                        num_of_people_total="2",
                        num_of_people_available="1"
                    )
        self.flat3 = FlatProfile.objects.create(
                        user=self.user3,
                        name="flat3",
                        place="AGH",
                        price=500,
                        time_of_staying_in_flat="1 MONTH",
                        num_of_people_total="2",
                        num_of_people_available="1"
                    )
        self.flat4 = FlatProfile.objects.create(
                        user=self.user4,
                        name="flat4",
                        place="AGH",
                        price=500,
                        time_of_staying_in_flat="1 MONTH",
                        num_of_people_total="2",
                        num_of_people_available="1"
                    )


    def test_view_list_flats(self):
        response1 = self.client.get(reverse('flats:view_list_flats'))
        response2 = self.client.post(reverse('flats:view_list_flats'), {'Flats': FlatProfile.objects.get(name="flat2")})

        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, self.flat1.name)

        self.assertEqual(response2.status_code, 200)


    def test_view_flat(self):
        response1 = self.client.get(reverse('flats:view_flat', args={2}))
        response2 = self.client.get(reverse('flats:view_flat', args={42}))

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 404)

    def test_my_flat(self):
        self.client.login(username='user1', password='secret')
        response1 = self.client.get(reverse('flats:my_flat'))

        self.assertEqual(response1.status_code, 302)
        self.assertRedirects(response1, reverse('flats:edit_flat'))


        self.client.login(username='user5', password='secret')
        response2 = self.client.get(reverse('flats:my_flat'))

        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse('flats:create_flat'))

    def test_create_flat(self):
        self.client.login(username='user5', password='secret')
        data = { 'name': "flat5",
                 'place': "AGH",
                 'price': 500,
                 'time_of_staying_in_flat': "1 MONTH",
                 'num_of_people_total': "2",
                 'num_of_people_available': "1"
        }

        response1 = self.client.get(reverse('flats:create_flat'))
        self.assertEqual(response1.status_code, 200)

        response2 = self.client.post(reverse('flats:create_flat'), data)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse('flats:view_list_flats'))

    def test_edit_flat(self):
        self.client.login(username='user1', password='secret')
        data = { 'name': "flat1 modified",
                 'place': "AGH",
                 'price': 1000,
                 'time_of_staying_in_flat': "1 MONTH",
                 'num_of_people_total': "2",
                 'num_of_people_available': "1",
                 'description': "test edit flat"
        }

        response1 = self.client.get(reverse('flats:edit_flat'))
        self.assertEqual(response1.status_code, 200)

        response2 = self.client.post(reverse('flats:edit_flat'), data)
        self.assertEqual(response2.status_code, 302)
        self.assertRedirects(response2, reverse('flats:view_list_flats'))
