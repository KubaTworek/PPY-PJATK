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
        category_entity = self.__find_category_by_name(category)
        if category_entity is None:
            category_id = self.__create_category(category)
        else:
            category_id = category_entity.get('Category_id')

        subcategory_entity = self.__find_subcategory_by_name_and_category_id(subcategory, category_id)
        if subcategory_entity is None:
            subcategory_id = self.__create_subcategory(subcategory, category_id)
        else:
            subcategory_id = subcategory_entity.get('Subcategory_id')

        question_entity = self.__create_question_entity(question, subcategory_id)
        for answer in answers_list:
            self.__create_answer(answer, question_entity.get('Question_id'))
        self.questions.append(question_entity)

    def generate_test(self, category, subcategory, num_questions):
        category_temp = self.__find_category_by_name(category)
        subcategory_temp = self.__find_subcategory_by_name_and_category_id(subcategory, category_temp.get('Category_id'))
        test_questions = [question for question in self.questions
                          if question['Subcategory_id'] == subcategory_temp.get('Subcategory_id')]
        random.shuffle(test_questions)
        questions_response = []
        for question_temp in test_questions:
            answers = self.__find_answers_by_question(question_temp)
            question_response = {
                'Question': question_temp.get('Question'),
                'Answers': answers
            }
            questions_response.append(question_response)
        return questions_response[:num_questions]

    def delete_category(self, name):
        category_temp = self.__find_category_by_name(name)
        subcategories = self.__find_subcategories_by_category_id(category_temp.get('Category_id'))
        questions = self.__find_questions_by_subcategories(subcategories)
        answers = self.__find_answers_by_questions(questions)
        self.categories = [category for category in self.categories if category['Category_id'] != category_temp.get('Category_id')]
        for subcategory_temp in subcategories:
            self.subcategories = [subcategory for subcategory in self.subcategories if subcategory['Subcategory_id'] == subcategory_temp.get('Subcategory_id')]
        for question_temp in questions:
            self.questions = [question for question in self.questions if question['Question_id'] == question_temp.get('Question_id')]
        for answer_temp in answers:
            self.answers = [answer for answer in self.answers if answer['Answer_id'] == answer_temp.get('Answer_id')]

    def delete_subcategory_by_name(self, subcategory_name, category_name):
        category_temp = self.__find_category_by_name(category_name)
        subcategories_to_delete = [subcategory for subcategory in self.subcategories if subcategory['Name'] == subcategory_name and subcategory['Category_id'] == category_temp.get('Category_id')]
        self.subcategories = [subcategory for subcategory in self.subcategories if subcategory['Name'] != subcategory_name and subcategory['Category_id'] != category_temp.get('Category_id')]
        questions = self.__find_questions_by_subcategories(subcategories_to_delete)
        answers = self.__find_answers_by_questions(questions)
        for question_temp in questions:
            self.questions = [question for question in self.questions if question['Question_id'] == question_temp.get('Question_id')]
        for answer_temp in answers:
            self.answers = [answer for answer in self.answers if answer['Answer_id'] == answer_temp.get('Answer_id')]

    def delete_question(self, name):
        questions_to_delete = [question for question in self.questions if question['Question'] == name]
        self.questions = [question for question in self.questions if question['Question'] != name]
        answers = self.__find_answers_by_questions(questions_to_delete)
        for answer_temp in answers:
            self.answers = [answer for answer in self.answers if answer['Answer_id'] == answer_temp.get('Answer_id')]

    def get_categories(self):
        return [category['Name'] for category in self.categories]

    def get_subcategories(self, category_name):
        category_temp = self.__find_category_by_name(category_name)
        return [subcategory['Name'] for subcategory in self.subcategories if subcategory['Category_id'] == category_temp.get('Category_id')]

    def __find_category_by_name(self, category):
        for category_temp in self.categories:
            if category_temp.get('Name') == category:
                return category_temp
        return None

    def __find_subcategory_by_name_and_category_id(self, subcategory, category_id):
        for subcategory_temp in self.subcategories:
            if subcategory_temp.get('Category_id') == category_id and subcategory_temp.get('Name') == subcategory:
                return subcategory_temp
        return self.__create_subcategory(subcategory, category_id)

    def __find_subcategories_by_category_id(self, category_id):
        subcategories = []
        for subcategory_temp in self.subcategories:
            if subcategory_temp.get('Category_id') == category_id:
                subcategories.append(subcategory_temp)
        return subcategories

    def __find_questions_by_subcategories(self, subcategories):
        questions = []
        for subcategory_temp in subcategories:
            subcategory_temp.append([question for question in self.questions if question['Subcategory_id'] != subcategory_temp.get('Subcategory_id')])
        return questions

    def __find_answers_by_questions(self, questions):
        answers = []
        for question_temp in questions:
            question_temp.append([answer for answer in self.answers if answer['Question_id'] != question_temp.get('Question_id')])
        return answers

    def __find_answers_by_question(self, question):
        return [answer for answer in self.answers if answer['Question_id'] == question.get('Question_id')]

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

    def __create_question_entity(self, question_text, subcategory_id):
        question_entity = {
            'Question_id': self.__question_id + 1,
            'Question': question_text,
            'Subcategory_id': subcategory_id
        }
        self.__question_id += 1
        return question_entity

    def __create_answer(self, answer, question_id):
        answer_entity = {
            'Answer_id': self.__answer_id + 1,
            'Answer': answer.get('content'),
            'IsCorrect': answer.get('is_correct'),
            'Question_id': question_id
        }
        self.__answer_id += 1
        self.answers.append(answer_entity)
