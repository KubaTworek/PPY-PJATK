import pyodbc


class Repository:
    def __init__(self):
        connection_string = "Driver={SQL Server};Server=db-mssql;Database=s25646;Trusted_Connection=yes;"
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def create_category(self, name):
        self.cursor.execute("SELECT MAX(Category_id) FROM Categories")
        max_category_id = self.cursor.fetchone()[0]
        category_id = max_category_id + 1 if max_category_id is not None else 1
        self.cursor.execute("INSERT INTO Categories (Category_id, Name) VALUES (?, ?)", (category_id, name))
        self.connection.commit()
        return category_id

    def create_subcategory(self, name, category_id):
        self.cursor.execute("SELECT MAX(Subcategory_id) FROM Subcategories")
        max_subcategory_id = self.cursor.fetchone()[0]
        subcategory_id = max_subcategory_id + 1 if max_subcategory_id is not None else 1
        self.cursor.execute("INSERT INTO Subcategories (Subcategory_id, Name, Category_id) VALUES (?, ?, ?)",
                            (subcategory_id, name, category_id))
        self.connection.commit()
        return subcategory_id

    def create_question(self, question_text, subcategory_id):
        self.cursor.execute("SELECT MAX(Question_id) FROM Questions")
        max_question_id = self.cursor.fetchone()[0]
        question_id = max_question_id + 1 if max_question_id is not None else 1
        self.cursor.execute("INSERT INTO Questions (Question_id, Question, Subcategory_id) VALUES (?, ?, ?)",
                            (question_id, question_text, subcategory_id))
        self.connection.commit()
        return question_id

    def create_answer(self, answer, question_id, is_correct):
        self.cursor.execute("SELECT MAX(Answer_id) FROM Answers")
        max_answer_id = self.cursor.fetchone()[0]
        answer_id = max_answer_id + 1 if max_answer_id is not None else 1
        self.cursor.execute("INSERT INTO Answers (Answer_id, Answer, Question_id, Is_correct) VALUES (?, ?, ?, ?)",
                            (answer_id, answer, question_id, is_correct))
        self.connection.commit()
        return answer_id

    def find_category_by_name(self, category):
        self.cursor.execute("SELECT * FROM Categories WHERE Name = ?", (category,))
        row = self.cursor.fetchone()
        if row:
            category_id, category_name = row
            return {
                'Category_id': category_id,
                'Name': category_name
            }
        return None

    def find_subcategory_by_name_and_category_id(self, subcategory, category_id):
        self.cursor.execute("SELECT * FROM Subcategories WHERE Name = ? AND Category_id = ?",
                            (subcategory, category_id))
        row = self.cursor.fetchone()
        if row:
            subcategory_id, subcategory_name, subcategory_category_id = row
            return {
                'Subcategory_id': subcategory_id,
                'Name': subcategory_name,
                'Category_id': subcategory_category_id
            }
        return None

    def find_subcategories_by_category_id(self, category_id):
        self.cursor.execute("SELECT * FROM Subcategories WHERE Category_id = ?", (category_id,))
        rows = self.cursor.fetchall()
        subcategories = []
        for row in rows:
            subcategory_id, subcategory_name, subcategory_category_id = row
            subcategory = {
                'Subcategory_id': subcategory_id,
                'Name': subcategory_name,
                'Category_id': subcategory_category_id
            }
            subcategories.append(subcategory)
        return subcategories

    def find_questions_by_subcategories(self, subcategories):
        subcategory_ids = [subcategory['Subcategory_id'] for subcategory in subcategories]
        placeholders = ",".join(["?"] * len(subcategory_ids))
        query = "SELECT * FROM Questions WHERE Subcategory_id IN ({})".format(placeholders)
        self.cursor.execute(query, subcategory_ids)
        rows = self.cursor.fetchall()
        questions = []
        for row in rows:
            question_id, question_text, question_subcategory_id = row
            question = {
                'Question_id': question_id,
                'Question': question_text,
                'Subcategory_id': question_subcategory_id
            }
            questions.append(question)
        return questions

    def find_answers_by_question(self, question_id):
        self.cursor.execute("SELECT * FROM Answers WHERE Question_id = ?", (question_id,))
        rows = self.cursor.fetchall()
        answers = []
        for row in rows:
            answer_id, answer_text, answer_is_correct, answer_question_id = row
            answer = {
                'Answer_id': answer_id,
                'Answer': answer_text,
                'Is_correct': answer_is_correct,
                'Question_id': answer_question_id
            }
            answers.append(answer)
        return answers

    def delete_category(self, category_id):
        self.cursor.execute("DELETE FROM Subcategories WHERE Category_id = ?", (category_id,))
        self.cursor.execute(
            "DELETE FROM Questions WHERE Subcategory_id IN (SELECT Subcategory_id FROM Subcategories WHERE Category_id = ?)",
            (category_id,))
        self.cursor.execute("DELETE FROM Categories WHERE Category_id = ?", (category_id,))
        self.connection.commit()

    def delete_subcategory(self, subcategory_id):
        self.cursor.execute("DELETE FROM Questions WHERE Subcategory_id = ?", (subcategory_id,))
        self.cursor.execute("DELETE FROM Subcategories WHERE Subcategory_id = ?", (subcategory_id,))
        self.connection.commit()

    def delete_question(self, question_id):
        self.cursor.execute("DELETE FROM Answers WHERE Question_id = ?", (question_id,))
        self.cursor.execute("DELETE FROM Questions WHERE Question_id = ?", (question_id,))
        self.connection.commit()

    def delete_answer(self, answer_id):
        self.cursor.execute("DELETE FROM Answers WHERE Answer_id = ?", (answer_id,))
        self.connection.commit()

    def get_categories(self):
        self.cursor.execute("SELECT Name FROM Categories")
        categories = [row.Name for row in self.cursor.fetchall()]
        return categories

    def get_subcategories(self, category_name):
        self.cursor.execute(
            "SELECT Subcategories.Name FROM Subcategories INNER JOIN Categories ON Subcategories.Category_id = Categories.Category_id WHERE Categories.Name = ?",
            (category_name,))
        subcategories = [row.Name for row in self.cursor.fetchall()]
        return subcategories

    def find_question_by_text(self, question_text):
        self.cursor.execute("SELECT * FROM Questions WHERE Question = ?", (question_text,))
        row = self.cursor.fetchone()
        if row:
            question_id, question_text, question_subcategory_id = row
            return {
                'Question_id': question_id,
                'Question': question_text,
                'Subcategory_id': question_subcategory_id
            }
        return None

    def close(self):
        self.cursor.close()
        self.connection.close()
