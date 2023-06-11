import sys
import unittest
import pyodbc

sys.path.append('C:/Users/kubat/IdeaProjects/PPY-PJATK/Quiz-App')
from Repository.SqlServerRepository import Repository


class RepositoryTests(unittest.TestCase):

    def setUp(self):
        connection_string = "Driver={SQL Server};Server=db-mssql;Database=s25646;Trusted_Connection=yes;"
        self.repository = Repository()
        self.connection = pyodbc.connect(connection_string)
        self.repository.cursor.execute("DROP TABLE Answers")
        self.repository.cursor.execute("DROP TABLE Questions")
        self.repository.cursor.execute("DROP TABLE Subcategories")
        self.repository.cursor.execute("DROP TABLE Categories")
        self.repository.cursor.execute("CREATE TABLE Categories (Category_id INT, Name VARCHAR(255))")
        self.repository.cursor.execute(
            "CREATE TABLE Subcategories (Subcategory_id INT, Name VARCHAR(255), Category_id INT)")
        self.repository.cursor.execute(
            "CREATE TABLE Questions (Question_id INT, Question VARCHAR(255), Subcategory_id INT)")
        self.repository.cursor.execute(
            "CREATE TABLE Answers (Answer_id INT, Answer VARCHAR(255), Is_correct BIT, Question_id INT)")

    def tearDown(self):
        self.repository.close()

    def test_create_category(self):
        # When
        category_id = self.repository.create_category("Category 1")

        # Then
        self.assertEqual(category_id, 1)

    def test_create_subcategory(self):
        # Given
        self.repository.create_category("Category 1")

        # When
        subcategory_id = self.repository.create_subcategory("Subcategory 1", 1)

        # Then
        self.assertEqual(subcategory_id, 1)

    def test_create_question(self):
        # Given
        self.repository.create_category("Category 1")
        self.repository.create_subcategory("Subcategory 1", 1)

        # When
        question_id = self.repository.create_question("Question 1", 1)

        # Then
        self.assertEqual(question_id, 1)

    def test_create_answer(self):
        # Given
        self.repository.create_category("Category 1")
        self.repository.create_subcategory("Subcategory 1", 1)
        self.repository.create_question("Question 1", 1)

        # When
        answer_id = self.repository.create_answer("Answer 1", 1, True)

        # Then
        self.assertEqual(answer_id, 1)

    def test_find_category_by_name(self):
        # Given
        self.repository.create_category("Category 1")

        # When
        category = self.repository.find_category_by_name("Category 1")

        # Then
        self.assertEqual(category['Category_id'], 1)
        self.assertEqual(category['Name'], 'Category 1')

    def test_find_subcategory_by_name_and_category_id(self):
        # Given
        self.repository.create_category("Category 1")
        self.repository.create_subcategory("Subcategory 1", 1)

        # When
        subcategory = self.repository.find_subcategory_by_name_and_category_id("Subcategory 1", 1)

        # Then
        self.assertEqual(subcategory['Subcategory_id'], 1)
        self.assertEqual(subcategory['Name'], 'Subcategory 1')
        self.assertEqual(subcategory['Category_id'], 1)

    def test_find_subcategories_by_category_id(self):
        # Given
        self.repository.create_category("Category 1")
        self.repository.create_subcategory("Subcategory 1", 1)
        self.repository.create_subcategory("Subcategory 2", 1)

        # When
        subcategories = self.repository.find_subcategories_by_category_id(1)

        # Then
        self.assertEqual(len(subcategories), 2)
        self.assertEqual(subcategories[0]['Subcategory_id'], 1)
        self.assertEqual(subcategories[0]['Name'], 'Subcategory 1')
        self.assertEqual(subcategories[0]['Category_id'], 1)
        self.assertEqual(subcategories[1]['Subcategory_id'], 2)
        self.assertEqual(subcategories[1]['Name'], 'Subcategory 2')
        self.assertEqual(subcategories[1]['Category_id'], 1)

    def test_find_questions_by_subcategories(self):
        # Given
        self.repository.create_category("Category 1")
        self.repository.create_subcategory("Subcategory 1", 1)
        self.repository.create_subcategory("Subcategory 2", 1)
        self.repository.create_question("Question 1", 1)
        self.repository.create_question("Question 2", 2)

        # When
        subcategories = [
            {
                'Subcategory_id': 1,
                'Name': 'Subcategory 1',
                'Category_id': 1
            },
            {
                'Subcategory_id': 2,
                'Name': 'Subcategory 2',
                'Category_id': 1
            }
        ]
        questions = self.repository.find_questions_by_subcategories(subcategories)

        # Then
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0]['Question_id'], 1)
        self.assertEqual(questions[0]['Question'], 'Question 1')
        self.assertEqual(questions[0]['Subcategory_id'], 1)
        self.assertEqual(questions[1]['Question_id'], 2)
        self.assertEqual(questions[1]['Question'], 'Question 2')
        self.assertEqual(questions[1]['Subcategory_id'], 2)

    def test_find_answers_by_question(self):
        # Given
        self.repository.cursor.execute(
            "INSERT INTO Questions (Question_id, Question, Subcategory_id) VALUES (1, 'Question 1', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (1, 'Answer 1', 1, 1)")
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (2, 'Answer 2', 0, 1)")

        # When
        answers = self.repository.find_answers_by_question(1)

        # Then
        self.assertEqual(len(answers), 2)
        self.assertEqual(answers[0]['Answer_id'], 1)
        self.assertEqual(answers[0]['Answer'], 'Answer 1')
        self.assertEqual(answers[0]['Is_correct'], 1)
        self.assertEqual(answers[0]['Question_id'], 1)
        self.assertEqual(answers[1]['Answer_id'], 2)
        self.assertEqual(answers[1]['Answer'], 'Answer 2')
        self.assertEqual(answers[1]['Is_correct'], 0)
        self.assertEqual(answers[1]['Question_id'], 1)

    def test_find_question_by_text(self):
        # Given
        self.repository.cursor.execute(
            "INSERT INTO Questions (Question_id, Question, Subcategory_id) VALUES (1, 'Question 1', 1)")

        # When
        question = self.repository.find_question_by_text('Question 1')

        # Then
        self.assertIsNotNone(question)
        self.assertEqual(question['Question_id'], 1)
        self.assertEqual(question['Question'], 'Question 1')
        self.assertEqual(question['Subcategory_id'], 1)

    def test_delete_category(self):
        # Given
        self.repository.cursor.execute("INSERT INTO Categories (Category_id, Name) VALUES (1, 'Category 1')")
        self.repository.cursor.execute(
            "INSERT INTO Subcategories (Subcategory_id, Name, Category_id) VALUES (1, 'Subcategory 1', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Subcategories (Subcategory_id, Name, Category_id) VALUES (2, 'Subcategory 2', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Questions (Question_id, Question, Subcategory_id) VALUES (1, 'Question 1', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Questions (Question_id, Question, Subcategory_id) VALUES (2, 'Question 2', 2)")
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (1, 'Answer 1', 1, 1)")
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (2, 'Answer 2', 0, 2)")

        # When
        self.repository.delete_category(1)

        # Then
        self.repository.cursor.execute("SELECT COUNT(*) FROM Categories")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 0)

        self.repository.cursor.execute("SELECT COUNT(*) FROM Subcategories")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 0)

        self.repository.cursor.execute("SELECT COUNT(*) FROM Questions")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 0)

        self.repository.cursor.execute("SELECT COUNT(*) FROM Answers")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 0)

    def test_delete_subcategory(self):
        # Given
        self.repository.cursor.execute(
            "INSERT INTO Subcategories (Subcategory_id, Name, Category_id) VALUES (1, 'Subcategory 1', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Subcategories (Subcategory_id, Name, Category_id) VALUES (2, 'Subcategory 2', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Questions (Question_id, Question, Subcategory_id) VALUES (1, 'Question 1', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Questions (Question_id, Question, Subcategory_id) VALUES (2, 'Question 2', 2)")
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (1, 'Answer 1', 1, 1)")
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (2, 'Answer 2', 0, 2)")

        # When
        self.repository.delete_subcategory(1)

        # Then
        self.repository.cursor.execute("SELECT COUNT(*) FROM Subcategories")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 1)

        self.repository.cursor.execute("SELECT COUNT(*) FROM Questions")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 1)

        self.repository.cursor.execute("SELECT COUNT(*) FROM Answers")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_delete_question(self):
        # Given
        self.repository.cursor.execute(
            "INSERT INTO Questions (Question_id, Question, Subcategory_id) VALUES (1, 'Question 1', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Questions (Question_id, Question, Subcategory_id) VALUES (2, 'Question 2', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (1, 'Answer 1', 1, 1)")
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (2, 'Answer 2', 0, 2)")

        # When
        self.repository.delete_question(1)

        # Then
        self.repository.cursor.execute("SELECT COUNT(*) FROM Questions")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 1)

        self.repository.cursor.execute("SELECT COUNT(*) FROM Answers")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_delete_answer(self):
        # Given
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (1, 'Answer 1', 1, 1)")
        self.repository.cursor.execute(
            "INSERT INTO Answers (Answer_id, Answer, Is_correct, Question_id) VALUES (2, 'Answer 2', 0, 1)")

        # When
        self.repository.delete_answer(1)

        # Then
        self.repository.cursor.execute("SELECT COUNT(*) FROM Answers")
        count = self.repository.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_get_categories(self):
        # Given
        self.repository.cursor.execute("INSERT INTO Categories (Category_id, Name) VALUES (1, 'Category 1')")
        self.repository.cursor.execute("INSERT INTO Categories (Category_id, Name) VALUES (2, 'Category 2')")

        # When
        categories = self.repository.get_categories()

        # Then
        self.assertEqual(len(categories), 2)
        self.assertIn('Category 1', categories)
        self.assertIn('Category 2', categories)

    def test_get_subcategories(self):
        # Given
        self.repository.cursor.execute("INSERT INTO Categories (Category_id, Name) VALUES (1, 'Category 1')")
        self.repository.cursor.execute(
            "INSERT INTO Subcategories (Subcategory_id, Name, Category_id) VALUES (1, 'Subcategory 1', 1)")
        self.repository.cursor.execute(
            "INSERT INTO Subcategories (Subcategory_id, Name, Category_id) VALUES (2, 'Subcategory 2', 1)")

        # When
        subcategories = self.repository.get_subcategories('Category 1')

        # Then
        self.assertEqual(len(subcategories), 2)
        self.assertIn('Subcategory 1', subcategories)
        self.assertIn('Subcategory 2', subcategories)
