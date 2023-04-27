class Repository:
    def __init__(self):
        self.__question_id = 0
        self.__category_id = 0
        self.__subcategory_id = 0
        self.__answer_id = 0
        self.questions = []
        self.categories = []
        self.subcategories = []
        self.answers = []

    def find_category_by_name(self, category):
        for category_temp in self.categories:
            if category_temp.get('Name') == category:
                return category_temp
        return None

    def find_subcategory_by_name_and_category_id(self, subcategory, category_id):
        for subcategory_temp in self.subcategories:
            if subcategory_temp.get('Category_id') == category_id and subcategory_temp.get('Name') == subcategory:
                return subcategory_temp
        return None

    def find_subcategories_by_category_id(self, category_id):
        subcategories = []
        for subcategory_temp in self.subcategories:
            if subcategory_temp.get('Category_id') == category_id:
                subcategories.append(subcategory_temp)
        return subcategories

    def find_questions_by_subcategories(self, subcategories):
        questions = []
        for subcategory_temp in subcategories:
            subcategory_temp.append([question for question in self.questions if question['Subcategory_id'] != subcategory_temp.get('Subcategory_id')])
        return questions

    def find_answers_by_questions(self, questions):
        answers = []
        for question_temp in questions:
            question_temp.append([answer for answer in self.answers if answer['Question_id'] != question_temp.get('Question_id')])
        return answers

    def find_answers_by_question(self, question):
        return [answer for answer in self.answers if answer['Question_id'] == question.get('Question_id')]

    def create_category(self, category):
        category_entity = {
            'Category_id': self.__category_id + 1,
            'Name': category
        }
        self.__category_id += 1
        self.categories.append(category_entity)
        return category_entity

    def create_subcategory(self, subcategory, category_id):
        subcategory_entity = {
            'Subcategory_id': self.__subcategory_id + 1,
            'Name': subcategory,
            'Category_id': category_id
        }
        self.__subcategory_id += 1
        self.subcategories.append(subcategory_entity)
        return subcategory_entity

    def create_question_entity(self, question_text, subcategory_id):
        question_entity = {
            'Question_id': self.__question_id + 1,
            'Question': question_text,
            'Subcategory_id': subcategory_id
        }
        self.__question_id += 1
        self.questions.append(question_entity)
        return question_entity

    def create_answer(self, answer, question_id):
        answer_entity = {
            'Answer_id': self.__answer_id + 1,
            'Answer': answer.get('content'),
            'Is_correct': answer.get('is_correct'),
            'Question_id': question_id
        }
        self.__answer_id += 1
        self.answers.append(answer_entity)