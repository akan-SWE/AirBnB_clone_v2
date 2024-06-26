#!/usr/bin/env python3
"""
Module: test_console

Additional test for the Console
"""
from io import StringIO
from unittest import TestCase
from console import HBNBCommand
from unittest.mock import patch, MagicMock


class TestConsole(TestCase):
    """ Test Cases for Console"""

    @patch("console.storage.save")
    @patch("console.HBNBCommand.classes", new_callable=dict)
    def test_do_create_inputs_validation(self, mock_classes, mock_save):
        """ Tests the parameters processing for the create command

        This checks handles the following cases:
            Replacing underscores (_) with spaces in the input string.
            Properly type casting string representations of integers and
            floats to their respective numeric types.
        Returns: None
        """
        args = ('ExistingClass param1="hello_world" param2=32 param3=4.0 '
                'param4=3.8.8')

        mock_instance = MagicMock()  # the instance
        # mock objects based on HBNBCommand.classes dictionary
        mock_classes["ExistingClass"] = lambda: mock_instance
        # act
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            HBNBCommand().do_create(args)
        # get the updated instance
        instance = mock_classes.get("ExistingClass")()
        # verify that value types are correctly set
        self.assertEqual(mock_instance.param1, "hello world")
        self.assertIsInstance(mock_instance.param2, int)
        self.assertIsInstance(mock_instance.param3, float)
        # param4 isn't an attribute because it doesn't fit the requirements
        self.assertFalse("param4" in mock_instance.__dict__)

        mock_save.assert_called_once()  # check if save is called
