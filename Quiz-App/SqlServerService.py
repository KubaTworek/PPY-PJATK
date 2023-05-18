import random

from SqlServerRepository import Repository


class Service:
    def __init__(self):
        self.repository = Repository()

    def create_question(self, category, subcategory, question, answers_list):
        category_entity = self.repository.find_category_by_name(category)
        if category_entity is None:
            category_id = self.repository.create_category(category)
        else:
            category_id = int(category_entity['Category_id'])

        subcategory_entity = self.repository.find_subcategory_by_name_and_category_id(subcategory, category_id)
        if subcategory_entity is None:
            subcategory_id = self.repository.create_subcategory(subcategory, category_id)
        else:
            subcategory_id = subcategory_entity['Subcategory_id']

        question_id = self.repository.create_question(question, subcategory_id)
        for answer in answers_list:
            self.repository.create_answer(answer['content'], question_id, answer['is_correct'])

    def generate_test(self, category, subcategory, num_questions):
        category_temp = self.repository.find_category_by_name(category)
        subcategory_temp = self.repository.find_subcategory_by_name_and_category_id(subcategory,
                                                                                    category_temp['Category_id'])
        if subcategory_temp is None:
            return None
        test_questions = self.repository.find_questions_by_subcategories([subcategory_temp])
        random.shuffle(test_questions)
        questions_response = []
        for question_temp in test_questions[:num_questions]:
            answers = self.repository.find_answers_by_question(question_temp['Question_id'])
            question_response = {
                'Question': question_temp['Question'],
                'Answers': answers
            }
            questions_response.append(question_response)
        return questions_response

    def delete_category(self, name):
        category_temp = self.repository.find_category_by_name(name)
        if category_temp is None:
            return
        subcategories = self.repository.find_subcategories_by_category_id(category_temp['Category_id'])
        questions = self.repository.find_questions_by_subcategories(subcategories)
        for question_temp in questions:
            self.repository.delete_question(question_temp['Question_id'])
        for subcategory_temp in subcategories:
            self.repository.delete_subcategory(subcategory_temp['Subcategory_id'])
        self.repository.delete_category(category_temp['Category_id'])

    def delete_subcategory_by_name(self, subcategory_name, category_name):
        category_temp = self.repository.find_category_by_name(category_name)
        if category_temp is None:
            return
        subcategory_temp = self.repository.find_subcategory_by_name_and_category_id(subcategory_name,
                                                                                    category_temp['Category_id'])
        if subcategory_temp is None:
            return
        questions = self.repository.find_questions_by_subcategories([subcategory_temp])
        for question_temp in questions:
            self.repository.delete_question(question_temp['Question_id'])
        self.repository.delete_subcategory(subcategory_temp['Subcategory_id'])

    def delete_question(self, question_text):
        question_temp = self.repository.find_question_by_text(question_text)
        if question_temp is None:
            return
        self.repository.delete_question(question_temp['Question_id'])

    def get_categories(self):
        return self.repository.get_categories()

    def get_subcategories(self, category_name):
        return self.repository.get_subcategories(category_name)
