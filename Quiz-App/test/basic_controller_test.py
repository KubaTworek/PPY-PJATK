import sys
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.append('C:/Users/kubat/IdeaProjects/PPY-PJATK/Quiz-App')
from Controller.BasicController import Controller


class ControllerTests(unittest.TestCase):

    def setUp(self):
        self.controller = Controller()

    def tearDown(self):
        pass

    @patch('builtins.input',
           side_effect=['Category 1', 'Subcategory 1', 'Question 1', 'Answer 1', 't', 'Answer 2', 'f', 'Answer 3', 'f',
                        'Answer 4', 'f'])
    def test_create_question(self, mock_input):
        self.controller.service.get_categories = lambda: []
        self.controller.service.get_subcategories = lambda category: []
        self.controller.service.create_question = lambda category, subcategory, question, answers: None

        self.controller.create_question()

        self.assertEqual(mock_input.call_count, 11)

    def test_generate_test(self, mock_input):
        pass

    @patch('builtins.input', side_effect=['Category 1'])
    def test_delete_category(self, mock_input):
        self.controller.service.get_categories = lambda: ['Category 1']
        self.controller.service.delete_category = lambda name: None

        self.controller.delete_category()

        self.assertEqual(mock_input.call_count, 1)

    @patch('builtins.input', side_effect=['Category 1', 'Subcategory 1'])
    def test_delete_subcategory(self, mock_input):
        self.controller.service.get_categories = lambda: ['Category 1']
        self.controller.service.get_subcategories = lambda category_name: ['Subcategory 1']
        self.controller.service.delete_subcategory_by_name = lambda subcategory_name, category_name: None

        self.controller.delete_subcategory()

        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input', side_effect=['Question 1'])
    def test_delete_question(self, mock_input):
        self.controller.service.delete_question = lambda name: None

        self.controller.delete_question()

        self.assertEqual(mock_input.call_count, 1)

    def test_quit_app(self):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with self.assertRaises(SystemExit) as cm:
                self.controller.quit_app()

            self.assertEqual(fake_output.getvalue(), "Dzieki za skorzystanie z naszej aplikacji!\n")
            self.assertEqual(cm.exception.code, 0)
