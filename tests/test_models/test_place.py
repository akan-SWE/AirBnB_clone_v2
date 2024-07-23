#!/usr/bin/env python3
"""Test for Place class"""
import unittest
from configs.env_vars import HBNB_TYPE_STORAGE
from models.model_registry import mapped_classes
from tests.test_models.test_base_model import test_basemodel


class test_Place(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'Place'
        self.value = mapped_classes['Place']

    def test_city_id(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'city_id'))

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'user_id'))

    def test_name(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'name'))

    def test_description(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'description'))

    def test_number_rooms(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'number_rooms'))

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'number_bathrooms'))

    def test_max_guest(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'max_guest'))

    def test_price_by_night(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'price_by_night'))

    def test_latitude(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'latitude'))

    def test_longitude(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'longitude'))

    def test_amenity_ids(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'amenity_ids'))

    @unittest.skipIf(HBNB_TYPE_STORAGE != 'db', reason='Requires database')
    def test_table_name(self):
        """ """
        self.assertEqual(self.value.__tablename__, 'places')

    def test_user_attr(self):
        """ """
        new = self.value()
        self.assertTrue(hasattr(self.value, 'user'))

    def test_reviews_attr(self):
        """ """
        self.assertTrue(hasattr(self.value, 'reviews'))

    @unittest.skipIf(HBNB_TYPE_STORAGE != 'db', reason='Requires database')
    def test_review_integrations_db(self):
        """Testing the interactions between each methods of the class"""

        state = mapped_classes['State']()
        state.name = 'Arizona'
        state.save()

        city = mapped_classes.get('City')()
        city.name = 'Phoenix'
        city.state_id = state.id
        city.save()

        user = mapped_classes.get('User')()
        user.first_name = 'John'
        user.last_name = 'Doe'
        user.password = '12345'
        user.email = 'johndoe@example.com'
        user.save()

        place = self.value()
        place.city_id = city.id
        place.user_id = user.id
        place.name = 'My home'
        place.latitude = 0.0
        place.longitude = 0.0
        place.description = 'Lorem ipsum dolor sit amet.'
        place.save()

        review = mapped_classes.get('Review')()
        review.text = 'Feels like home'
        review.place_id = place.id
        review.user_id = user.id
        review.save()

        self.assertEqual(place.reviews, [review])

    def test_reviews_integrations_file(self):
        """ """
        place = self.value()
        place.save()
        review = mapped_classes.get('Review')()

        review.place_id = place.id
        review.save()

        self.assertEqual(place.reviews, [review])
