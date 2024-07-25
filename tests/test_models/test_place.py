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

    @unittest.skipIf(HBNB_TYPE_STORAGE == 'file', reason='Requires database')
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

    @unittest.skipIf(HBNB_TYPE_STORAGE == 'file', reason='Requires database')
    def test_reviews_attr_integration_db(self):
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

    @unittest.skipIf(HBNB_TYPE_STORAGE == 'db', reason='Requires file engine')
    def test_place_and_review_relationship_file(self):
        """ """
        place = self.value()
        place.save()
        review = mapped_classes.get('Review')()
        review.text = 'So tiny'
        review.place_id = place.id
        review.save()

        self.assertEqual(place.reviews, [review])

    def test_amenities_attr(self):
        self.assertTrue(hasattr(self.value, 'amenities'))

    @unittest.skipIf(HBNB_TYPE_STORAGE == 'file', reason='Requires database')
    def test_place_and_amenity_relationship_db(self):

        from models.place import place_amenity
        state = mapped_classes['State']()
        state.name = 'Lagos'
        state.save()

        city = mapped_classes.get('City')()
        city.name = 'Lagos'
        city.state_id = state.id
        city.save()

        user = mapped_classes.get('User')()
        user.first_name = 'Cat'
        user.last_name = 'Dog'
        user.password = '12345'
        user.email = 'catDog@example.com'
        user.save()

        place1 = self.value()
        place1.city_id = city.id
        place1.user_id = user.id
        place1.name = 'Tiny home'
        place1.latitude = 0.0
        place1.longitude = 0.0
        place1.description = 'Lorem ipsum dolor sit amet.'

        place2 = self.value()
        place2.city_id = city.id
        place2.user_id = user.id
        place2.name = 'Tiny home'
        place2.latitude = 0.0
        place2.longitude = 0.0
        place2.description = 'Lorem ipsum dolor sit amet.'

        amenity1 = mapped_classes['Amenity']()
        amenity1.name = 'Wifi'
        amenity1.save()

        amenity1.place_amenities.append(place1)
        amenity1.place_amenities.append(place2)
        amenity1.save()

        self.assertIn(place1, amenity1.place_amenities)
        self.assertIn(place2, amenity1.place_amenities)
        self.assertIn(amenity1, place1.amenities)

    @unittest.skipIf(HBNB_TYPE_STORAGE == 'db', reason='Requires file engine')
    def test_amenities_getter_and_setter(self):
        """ """
        amenity = mapped_classes['Amenity']()
        place = mapped_classes['Place']()
        place.amenities.append(amenity)

        self.assertIsInstance(place.amenities, list)
        self.assertIn(amenity, place.amenities)
