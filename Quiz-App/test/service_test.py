import sys

sys.path.append('C:/Users/kubat/IdeaProjects/PPY-PJATK/Quiz-App')

import unittest
from unittest.mock import MagicMock

from Service.Service import Service


class ServiceTests(unittest.TestCase):

    def setUp(self):
        repository_mock = MagicMock()

        self.service = Service()
        self.service.repository = repository_mock
        pass

    def tearDown(self):
        pass

    def test_create_question(self):
        # Given
        category = 'Category'
        subcategory = 'Subcategory'
        question = 'Question'
        answers_list = [
            {'content': 'Answer 1', 'is_correct': True},
            {'content': 'Answer 2', 'is_correct': False},
            {'content': 'Answer 3', 'is_correct': False}
        ]

        self.service.repository.find_category_by_name.return_value = None
        self.service.repository.create_category.return_value = 1
        self.service.repository.find_subcategory_by_name_and_category_id.return_value = None
        self.service.repository.create_subcategory.return_value = 2
        self.service.repository.create_question.return_value = 3

        # When
        self.service.create_question(category, subcategory, question, answers_list)

        # Then
        self.service.repository.find_category_by_name.assert_called_once_with(category)
        self.service.repository.create_category.assert_called_once_with(category)
        self.service.repository.find_subcategory_by_name_and_category_id.assert_called_once_with(subcategory, 1)
        self.service.repository.create_subcategory.assert_called_once_with(subcategory, 1)
        self.service.repository.create_question.assert_called_once_with(question, 2)
        self.service.repository.create_answer.assert_called()
        self.assertEqual(self.service.repository.create_answer.call_count, len(answers_list))

        expected_calls = [
            unittest.mock.call('Answer 1', 3, True),
            unittest.mock.call('Answer 2', 3, False),
            unittest.mock.call('Answer 3', 3, False)
        ]
        self.service.repository.create_answer.assert_has_calls(expected_calls)

    def test_generate_test(self):
        # Given
        category = 'Category'
        subcategory = 'Subcategory'
        num_questions = 5

        self.service.repository.find_category_by_name.return_value = {'Category_id': 1}
        self.service.repository.find_subcategory_by_name_and_category_id.return_value = {'Subcategory_id': 2}
        self.service.repository.find_questions_by_subcategories.return_value = [
            {'Question_id': 1, 'Question': 'Question 1'},
            {'Question_id': 2, 'Question': 'Question 2'},
            {'Question_id': 3, 'Question': 'Question 3'},
            {'Question_id': 4, 'Question': 'Question 4'},
            {'Question_id': 5, 'Question': 'Question 5'}
        ]
        self.service.repository.find_answers_by_question.side_effect = [
            [{'Answer_id': 1, 'content': 'Answer 1', 'is_correct': True}],
            [{'Answer_id': 2, 'content': 'Answer 2', 'is_correct': False}],
            [{'Answer_id': 3, 'content': 'Answer 3', 'is_correct': True}],
            [{'Answer_id': 4, 'content': 'Answer 4', 'is_correct': False}],
            [{'Answer_id': 5, 'content': 'Answer 5', 'is_correct': True}]
        ]

        # When
        result = self.service.generate_test(category, subcategory, num_questions)

        # Then
        self.service.repository.find_category_by_name.assert_called_once_with(category)
        self.service.repository.find_subcategory_by_name_and_category_id.assert_called_once_with(subcategory, 1)
        self.service.repository.find_questions_by_subcategories.assert_called_once_with([{'Subcategory_id': 2}])
        self.assertEqual(self.service.repository.find_answers_by_question.call_count, num_questions)

        self.assertEqual(num_questions, len(result))

    def test_delete_category(self):
        # Given
        category_name = 'Category'

        category_id = 1
        category_temp = {'Category_id': category_id}
        self.service.repository.find_category_by_name.return_value = category_temp
        self.service.repository.find_subcategories_by_category_id.return_value = [
            {'Subcategory_id': 2},
            {'Subcategory_id': 3}
        ]
        self.service.repository.find_questions_by_subcategories.return_value = [
            {'Question_id': 4},
            {'Question_id': 5},
            {'Question_id': 6}
        ]

        # When
        self.service.delete_category(category_name)

        # Then
        self.service.repository.find_category_by_name.assert_called_once_with(category_name)
        self.service.repository.find_subcategories_by_category_id.assert_called_once_with(category_id)
        self.service.repository.find_questions_by_subcategories.assert_called_once_with([
            {'Subcategory_id': 2},
            {'Subcategory_id': 3}
        ])
        expected_delete_calls = [
            unittest.mock.call(4),
            unittest.mock.call(5),
            unittest.mock.call(6)
        ]
        self.service.repository.delete_question.assert_has_calls(expected_delete_calls)
        expected_delete_subcategory_calls = [
            unittest.mock.call(2),
            unittest.mock.call(3)
        ]
        self.service.repository.delete_subcategory.assert_has_calls(expected_delete_subcategory_calls)
        self.service.repository.delete_category.assert_called_once_with(category_id)

    def test_subcategory_by_name(self):
        # Given
        subcategory_name = 'Subcategory'
        category_name = 'Category'

        category_id = 1
        category_temp = {'Category_id': category_id}
        subcategory_id = 2
        subcategory_temp = {'Subcategory_id': subcategory_id}
        self.service.repository.find_category_by_name.return_value = category_temp
        self.service.repository.find_subcategory_by_name_and_category_id.return_value = subcategory_temp
        self.service.repository.find_questions_by_subcategories.return_value = [
            {'Question_id': 3},
            {'Question_id': 4},
            {'Question_id': 5}
        ]

        # When
        self.service.delete_subcategory_by_name(subcategory_name, category_name)

        # Then
        self.service.repository.find_category_by_name.assert_called_once_with(category_name)
        self.service.repository.find_subcategory_by_name_and_category_id.assert_called_once_with(
            subcategory_name, category_id
        )
        self.service.repository.find_questions_by_subcategories.assert_called_once_with([subcategory_temp])
        expected_delete_calls = [
            unittest.mock.call(3),
            unittest.mock.call(4),
            unittest.mock.call(5)
        ]
        self.service.repository.delete_question.assert_has_calls(expected_delete_calls)
        self.service.repository.delete_subcategory.assert_called_once_with(subcategory_id)

    def test_delete_question(self):
        # Given
        question_text = 'Question'

        question_id = 1
        question_temp = {'Question_id': question_id}
        self.service.repository.find_question_by_text.return_value = question_temp

        # When
        self.service.delete_question(question_text)

        # Then
        self.service.repository.find_question_by_text.assert_called_once_with(question_text)
        self.service.repository.delete_question.assert_called_once_with(question_id)

    def test_get_categories(self):
        # Given
        expected_categories = ['Category 1', 'Category 2', 'Category 3']
        self.service.repository.get_categories.return_value = expected_categories

        # When
        result = self.service.get_categories()

        # Then
        self.assertEqual(result, expected_categories)
        self.service.repository.get_categories.assert_called_once()

    def test_get_subcategories(self):
        # Given
        category_name = 'Category'

        expected_subcategories = ['Subcategory 1', 'Subcategory 2', 'Subcategory 3']
        self.service.repository.get_subcategories.return_value = expected_subcategories

        # When
        result = self.service.get_subcategories(category_name)

        # Then
        self.assertEqual(result, expected_subcategories)
        self.service.repository.get_subcategories.assert_called_once_with(category_name)


if __name__ == '__main__':
    unittest.main()
