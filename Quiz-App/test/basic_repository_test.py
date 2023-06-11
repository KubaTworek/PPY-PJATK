import sys
import unittest

sys.path.append('C:/Users/kubat/IdeaProjects/PPY-PJATK/Quiz-App')
from Repository.BasicRepository import Repository


class BasicRepositoryTests(unittest.TestCase):

    def setUp(self):
        self.repository = Repository()
        self.repository.categories = [{'Category_id': 1, 'Name': 'Category 1'},
                                      {'Category_id': 2, 'Name': 'Category 2'}]
        self.repository.subcategories = [{'Subcategory_id': 1, 'Name': 'Subcategory 1', 'Category_id': 1},
                                         {'Subcategory_id': 2, 'Name': 'Subcategory 2', 'Category_id': 1},
                                         {'Subcategory_id': 3, 'Name': 'Subcategory 3', 'Category_id': 2}]
        self.repository.questions = [{'Question_id': 1, 'Question': 'Question 1', 'Subcategory_id': 1},
                                     {'Question_id': 2, 'Question': 'Question 2', 'Subcategory_id': 2}]
        self.repository.answers = [{'Answer_id': 1, 'Answer': 'Answer 1', 'Is_correct': True, 'Question_id': 1},
                                   {'Answer_id': 2, 'Answer': 'Answer 2', 'Is_correct': False, 'Question_id': 1},
                                   {'Answer_id': 3, 'Answer': 'Answer 3', 'Is_correct': True, 'Question_id': 2}]
        pass

    def tearDown(self):
        pass

    def test_create_category(self):
        # Given
        category = 'New Category'

        # When
        new_category_id = self.repository.create_category(category)

        # Then
        self.assertEqual(new_category_id, 3)
        self.assertEqual(len(self.repository.categories), 3)
        new_category = self.repository.categories[2]
        self.assertEqual(new_category['Category_id'], 3)
        self.assertEqual(new_category['Name'], category)

    def test_create_subcategory(self):
        # Given
        subcategory = 'New Subcategory'
        category_id = 1

        # When
        new_subcategory_id = self.repository.create_subcategory(subcategory, category_id)

        # Then
        self.assertEqual(new_subcategory_id, 4)
        self.assertEqual(len(self.repository.subcategories), 4)
        new_subcategory = self.repository.subcategories[3]
        self.assertEqual(new_subcategory['Subcategory_id'], 4)
        self.assertEqual(new_subcategory['Name'], subcategory)
        self.assertEqual(new_subcategory['Category_id'], category_id)

    def test_create_question(self):
        # Given
        question_text = 'New Question'
        subcategory_id = 1

        # When
        new_question_id = self.repository.create_question(question_text, subcategory_id)

        # Then
        self.assertEqual(new_question_id, 3)
        self.assertEqual(len(self.repository.questions), 3)
        new_question = self.repository.questions[2]
        self.assertEqual(new_question['Question_id'], 3)
        self.assertEqual(new_question['Question'], question_text)
        self.assertEqual(new_question['Subcategory_id'], subcategory_id)

    def test_create_answer(self):
        # Given
        answer = 'New Answer'
        question_id = 1
        is_correct = True

        # When
        new_answer_id = self.repository.create_answer(answer, question_id, is_correct)

        # Then
        self.assertEqual(new_answer_id, 4)
        self.assertEqual(len(self.repository.answers), 4)
        new_answer = self.repository.answers[3]
        self.assertEqual(new_answer['Answer_id'], 4)
        self.assertEqual(new_answer['Answer'], answer)
        self.assertEqual(new_answer['Is_correct'], is_correct)
        self.assertEqual(new_answer['Question_id'], question_id)

    def test_find_category_by_name(self):
        # Given
        category_name = 'Category 1'

        # When
        result = self.repository.find_category_by_name(category_name)

        # Then
        self.assertIsNotNone(result)
        self.assertEqual(result['Category_id'], 1)
        self.assertEqual(result['Name'], category_name)

    def test_find_subcategory_by_name_and_category_id(self):
        # Given
        subcategory_name = 'Subcategory 2'
        category_id = 1

        # When
        result = self.repository.find_subcategory_by_name_and_category_id(subcategory_name, category_id)

        # Then
        self.assertIsNotNone(result)
        self.assertEqual(result['Subcategory_id'], 2)
        self.assertEqual(result['Name'], subcategory_name)
        self.assertEqual(result['Category_id'], category_id)

    def test_find_subcategories_by_category_id(self):
        # Given
        category_id = 1

        # When
        result = self.repository.find_subcategories_by_category_id(category_id)

        # Then
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Subcategory_id'], 1)
        self.assertEqual(result[1]['Subcategory_id'], 2)
        self.assertEqual(result[0]['Category_id'], category_id)
        self.assertEqual(result[1]['Category_id'], category_id)

    def test_find_questions_by_subcategories(self):
        # Given
        subcategories = [{'Subcategory_id': 1}, {'Subcategory_id': 2}]

        # When
        result = self.repository.find_questions_by_subcategories(subcategories)

        # Then
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Question_id'], 1)
        self.assertEqual(result[1]['Question_id'], 2)
        self.assertEqual(result[0]['Subcategory_id'], subcategories[0]['Subcategory_id'])
        self.assertEqual(result[1]['Subcategory_id'], subcategories[1]['Subcategory_id'])

    def test_find_answers_by_question(self):
        # Given
        question_id = 1

        # When
        result = self.repository.find_answers_by_question(question_id)

        # Then
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Answer_id'], 1)
        self.assertEqual(result[1]['Answer_id'], 2)
        self.assertEqual(result[0]['Question_id'], question_id)
        self.assertEqual(result[1]['Question_id'], question_id)

    def test_find_question_by_text(self):
        # Given
        question_text = 'Question 1'

        # When
        result = self.repository.find_question_by_text(question_text)

        # Then
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['Question_id'], 1)
        self.assertEqual(result[0]['Question'], question_text)

    def test_delete_category(self):
        # Given
        category_id = 1

        # When
        self.repository.delete_category(category_id)

        # Then
        self.assertEqual(len(self.repository.categories), 1)
        self.assertEqual(len(self.repository.subcategories), 1)
        self.assertEqual(len(self.repository.questions), 0)
        self.assertEqual(len(self.repository.answers), 0)

    def test_delete_subcategory(self):
        # Given
        subcategory_id = 1

        # When
        self.repository.delete_subcategory(subcategory_id)

        # Then
        self.assertEqual(len(self.repository.subcategories), 2)
        self.assertEqual(len(self.repository.questions), 1)
        self.assertEqual(len(self.repository.answers), 1)

    def test_delete_question(self):
        # Given
        question_id = 1

        # When
        self.repository.delete_question(question_id)

        # Then
        self.assertEqual(len(self.repository.questions), 1)
        self.assertEqual(len(self.repository.answers), 1)

    def test_delete_answer(self):
        # Given
        answer_id = 1

        # When
        self.repository.delete_answer(answer_id)

        # Then
        self.assertEqual(len(self.repository.answers), 2)

    def test_get_categories(self):
        # When
        categories = self.repository.get_categories()

        # Then
        self.assertEqual(len(categories), 2)
        self.assertIn('Category 1', categories)
        self.assertIn('Category 2', categories)

    def test_get_subcategories(self):
        # Given
        category_name = 'Category 1'

        # When
        subcategories = self.repository.get_subcategories(category_name)

        # Then
        self.assertEqual(len(subcategories), 2)
        self.assertIn('Subcategory 1', subcategories)
        self.assertIn('Subcategory 2', subcategories)
