#!/usr/bin/env python3
"""
Module: test_console

Additional test for the Console
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock
from io import StringIO


class TestConsole(TestCase):
    """ Test Cases for Console"""

    @patch('sys.stdout', new_callable=StringIO)
    @patch("models.model_registry.mapped_classes", new_callable=dict)
    def test_do_create_inputs_validation(self, mock_classes, mock_stdout):
        """ Tests the parameters processing for the create command

        This checks handles the following cases:
            Replacing underscores (_) with spaces in the input string.
            Properly type casting string representations of integers and
            floats to their respective numeric types.
        Returns: None
        """
        from console import HBNBCommand

        args = ('ExistingClass param1="hello_world" param2=32 param3=4.0 '
                'param4=3.8.8')

        mock_instance = MagicMock()  # the instance
        # mock objects based on HBNBCommand.classes dictionary
        mock_classes["ExistingClass"] = lambda: mock_instance
        # act
        # with patch.object(mock_instance, 'save') as mock_save:
        #     mock_save.assert_called_once()  # check if save is called
        HBNBCommand().do_create(args)
        # verify that value types are correctly set
        self.assertEqual(mock_instance.param1, "hello world")
        self.assertIsInstance(mock_instance.param2, int)
        self.assertIsInstance(mock_instance.param3, float)
        # param4 isn't an attribute because it doesn't fit the requirements
        self.assertFalse("param4" in mock_instance.__dict__)
