import random


class Service:
    def __init__(self):
        self.__question_id = 0
        self.__category_id = 0
        self.__subcategory_id = 0
        self.__answer_id = 0
        self.questions = []
        self.categories = []
        self.subcategories = []
        self.answers = []

    def create_question(self, category, subcategory, question, answers_list):
        category_entity = self.find_category_by_name(category)
        if category_entity is None:
            category_id = self.__create_category(category)
        else:
            category_id = category_entity.get('Category_id')

        subcategory_entity = self.find_subcategory_by_name_and_category_id(subcategory, category_id)
        if subcategory_entity is None:
            subcategory_id = self.__create_subcategory(subcategory, category_id)
        else:
            subcategory_id = subcategory_entity.get('Subcategory_id')

        question_entity = self.__create_question_entity(question, subcategory_id)
        for answer in answers_list:
            self.__create_answer(answer, question_entity.get('Question_id'))
        self.questions.append(question_entity)

    def __create_category(self, category):
        category_entity = {
            'Category_id': self.__category_id + 1,
            'Name': category
        }
        self.__category_id += 1
        self.categories.append(category_entity)
        return category_entity

    def __create_subcategory(self, subcategory, category_id):
        subcategory_entity = {
            'Subcategory_id': self.__subcategory_id + 1,
            'Name': subcategory,
            'Category_id': category_id
        }
        self.__subcategory_id += 1
        self.subcategories.append(subcategory_entity)
        return subcategory_entity

    def __create_answer(self, answer, question_id):
        answer_entity = {
            'Answer_id': self.__answer_id + 1,
            'Answer': answer.get('content'),
            'IsCorrect': answer.get('is_correct'),
            'Question_id': question_id
        }
        self.answers.append(answer_entity)

    def generate_test(self, category, subcategory, num_questions):
        if category is None and subcategory is None:
            test_questions = self.questions
        elif category is None:
            test_questions = [question for question in self.questions
                              if question['subcategory'] == subcategory]
        elif subcategory is None:
            test_questions = [question for question in self.questions
                              if question['category'] == category]
        else:
            test_questions = [question for question in self.questions
                              if question['category'] == category
                              and question['subcategory'] == subcategory]
        random.shuffle(test_questions)
        return test_questions[:num_questions]

    def delete_category(self, name):
        self.questions = [question for question in self.questions if question['category'] != name]

    def delete_subcategory(self, name):
        self.questions = [question for question in self.questions if question['subcategory'] != name]

    def delete_question(self, name):
        self.questions = [question for question in self.questions if question['question'] != name]

    def get_categories(self):
        return set([q['category'] for q in self.questions])

    def get_subcategories(self, category):
        return set([q['subcategory'] for q in self.questions if q['category'] == category])

    def find_category_by_name(self, category):
        for category_temp in self.categories:
            if category_temp.get('Name') == category:
                return category_temp
        return None

    def find_subcategory_by_name_and_category_id(self, subcategory, category_id):
        for subcategory_temp in self.subcategories:
            if subcategory_temp.get('Category_id') == category_id and subcategory_temp.get('Name') == subcategory:
                return subcategory_temp
        return self.__create_subcategory(subcategory, category_id)

    def __create_question_entity(self, question_text, subcategory_id):
        question_entity = {
            'Question_id': self.__question_id + 1,
            'Question': question_text,
            'Subcategory_id': subcategory_id
        }
        self.__question_id += 1
        return question_entity
