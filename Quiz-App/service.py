import random

from repository import Repository


class Service:
    def __init__(self):
        self.repository = Repository()

    def create_question(self, category, subcategory, question, answers_list):
        category_entity = self.repository.find_category_by_name(category)
        if category_entity is None:
            category_id = self.repository.create_category(category).get('Category_id')
        else:
            category_id = category_entity.get('Category_id')

        subcategory_entity = self.repository.find_subcategory_by_name_and_category_id(subcategory, category_id)
        if subcategory_entity is None:
            subcategory_id = self.repository.create_subcategory(subcategory, category_id).get('Subcategory_id')
        else:
            subcategory_id = subcategory_entity.get('Subcategory_id')

        question_entity = self.repository.create_question_entity(question, subcategory_id)
        for answer in answers_list:
            self.repository.create_answer(answer, question_entity.get('Question_id'))

    def generate_test(self, category, subcategory, num_questions):
        category_temp = self.repository.find_category_by_name(category)
        subcategory_temp = self.repository.find_subcategory_by_name_and_category_id(subcategory, category_temp.get('Category_id'))
        if subcategory_temp is None:
            return None
        test_questions = [question for question in self.repository.questions
                          if question['Subcategory_id'] == subcategory_temp.get('Subcategory_id')]
        random.shuffle(test_questions)
        questions_response = []
        for question_temp in test_questions:
            answers = self.repository.find_answers_by_question(question_temp)
            question_response = {
                'Question': question_temp.get('Question'),
                'Answers': answers
            }
            questions_response.append(question_response)
        return questions_response[:num_questions]

    def delete_category(self, name):
        category_temp = self.repository.find_category_by_name(name)
        subcategories = self.repository.find_subcategories_by_category_id(category_temp.get('Category_id'))
        questions = self.repository.find_questions_by_subcategories(subcategories)
        answers = self.repository.find_answers_by_questions(questions)
        self.repository.categories = [category for category in self.repository.categories if category['Category_id'] != category_temp.get('Category_id')]
        for subcategory_temp in subcategories:
            self.repository.subcategories = [subcategory for subcategory in self.repository.subcategories if subcategory['Subcategory_id'] == subcategory_temp.get('Subcategory_id')]
        for question_temp in questions:
            self.repository.questions = [question for question in self.repository.questions if question['Question_id'] == question_temp.get('Question_id')]
        for answer_temp in answers:
            self.repository.answers = [answer for answer in self.repository.answers if answer['Answer_id'] == answer_temp.get('Answer_id')]

    def delete_subcategory_by_name(self, subcategory_name, category_name):
        category_temp = self.repository.find_category_by_name(category_name)
        subcategories_to_delete = [subcategory for subcategory in self.repository.subcategories if subcategory['Name'] == subcategory_name and subcategory['Category_id'] == category_temp.get('Category_id')]
        self.repository.subcategories = [subcategory for subcategory in self.repository.subcategories if subcategory['Name'] != subcategory_name and subcategory['Category_id'] != category_temp.get('Category_id')]
        questions = self.repository.find_questions_by_subcategories(subcategories_to_delete)
        answers = self.repository.find_answers_by_questions(questions)
        for question_temp in questions:
            self.repository.questions = [question for question in self.repository.questions if question['Question_id'] == question_temp.get('Question_id')]
        for answer_temp in answers:
            self.repository.answers = [answer for answer in self.repository.answers if answer['Answer_id'] == answer_temp.get('Answer_id')]

    def delete_question(self, name):
        questions_to_delete = [question for question in self.repository.questions if question['Question'] == name]
        self.repository.questions = [question for question in self.repository.questions if question['Question'] != name]
        answers = self.repository.find_answers_by_questions(questions_to_delete)
        for answer_temp in answers:
            self.repository.answers = [answer for answer in self.repository.answers if answer['Answer_id'] == answer_temp.get('Answer_id')]

    def get_categories(self):
        return [category['Name'] for category in self.repository.categories]

    def get_subcategories(self, category_name):
        category_temp = self.repository.find_category_by_name(category_name)
        if category_temp is not None:
            return [subcategory['Name'] for subcategory in self.repository.subcategories if subcategory['Category_id'] == category_temp.get('Category_id')]
