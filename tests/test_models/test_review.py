#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.model_registry import mapped_classes
# from models.review import Review


class test_review(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'Review'
        self.value = mapped_classes[self.name]

    def test_table_name(self):
        """Check that table name is exists and is set to reviews"""
        self.assertEqual(self.value.__tablename__, 'reviews')

    def test_text_column_exists(self):
        """Verify that text column exists"""
        self.assertTrue(hasattr(self.value, 'text'))

    def test_place_id_column_exists(self):
        """Test place_id colun exists"""
        self.assertTrue(hasattr(self.value, 'place_id'))

    def test_user_id_column_exists(self):
        """Test user_id column exists"""
        self.assertTrue(hasattr(self.value, 'user_id'))
