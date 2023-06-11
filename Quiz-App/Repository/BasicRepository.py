class Repository:
    def __init__(self):
        self.questions = []
        self.categories = []
        self.subcategories = []
        self.answers = []

    def create_category(self, category):
        category_entity = {
            'Category_id': len(self.categories) + 1,
            'Name': category
        }
        self.categories.append(category_entity)
        return category_entity.get('Category_id')

    def create_subcategory(self, subcategory, category_id):
        subcategory_entity = {
            'Subcategory_id': len(self.subcategories) + 1,
            'Name': subcategory,
            'Category_id': category_id
        }
        self.subcategories.append(subcategory_entity)
        return subcategory_entity.get('Subcategory_id')

    def create_question(self, question_text, subcategory_id):
        question_entity = {
            'Question_id': len(self.questions) + 1,
            'Question': question_text,
            'Subcategory_id': subcategory_id
        }
        self.questions.append(question_entity)
        return question_entity.get('Question_id')

    def create_answer(self, answer, question_id, is_correct):
        answer_entity = {
            'Answer_id': len(self.answers) + 1,
            'Answer': answer,
            'Is_correct': is_correct,
            'Question_id': question_id
        }
        self.answers.append(answer_entity)
        return answer_entity.get('Answer_id')

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
            for question_temp in self.questions:
                if question_temp['Subcategory_id'] == subcategory_temp.get('Subcategory_id'):
                    questions.append(question_temp)
        return questions

    def find_answers_by_question(self, question_id):
        answers = []
        for answer_temp in self.answers:
            if answer_temp['Question_id'] == question_id:
                answers.append(answer_temp)
        return answers

    def find_question_by_text(self, question_text):
        return [question for question in self.questions if question['Question'] == question_text]

    def delete_category(self, category_id):
        category_temp = self.__find_category_by_id(category_id)
        if category_temp is not None:
            self.categories.remove(category_temp)
            subcategories_to_remove = [subcategory for subcategory in self.subcategories if
                                       subcategory.get('Category_id') == category_id]
            subcategory_ids_to_remove = [subcategory.get('Subcategory_id') for subcategory in subcategories_to_remove]
            self.subcategories = [subcategory for subcategory in self.subcategories if
                                  subcategory.get('Category_id') != category_id]
            questions_to_remove = [question for question in self.questions if
                                   question.get('Subcategory_id') in subcategory_ids_to_remove]
            question_ids_to_remove = [question.get('Question_id') for question in questions_to_remove]
            self.questions = [question for question in self.questions if
                              question.get('Subcategory_id') not in subcategory_ids_to_remove]
            self.answers = [answer for answer in self.answers if
                            answer.get('Question_id') not in question_ids_to_remove]

    def delete_subcategory(self, subcategory_id):
        subcategory_temp = self.__find_subcategory_by_id(subcategory_id)
        if subcategory_temp is not None:
            self.subcategories.remove(subcategory_temp)
            question_ids_to_remove = [question.get('Question_id') for question in self.questions if
                                      question.get('Subcategory_id') == subcategory_id]
            self.answers = [answer for answer in self.answers if
                            answer.get('Question_id') not in question_ids_to_remove]
            self.questions = [question for question in self.questions if
                              question.get('Subcategory_id') != subcategory_id]


    def delete_question(self, question_id):
        question_temp = self.__find_question_by_id(question_id)
        if question_temp is not None:
            self.questions.remove(question_temp)
            self.answers = [answer for answer in self.answers if answer.get('Question_id') != question_id]

    def delete_answer(self, answer_id):
        answer_temp = self.__find_answer_by_id(answer_id)
        if answer_temp is not None:
            self.answers.remove(answer_temp)

    def get_categories(self):
        return [category['Name'] for category in self.categories]

    def get_subcategories(self, category_name):
        category_temp = self.find_category_by_name(category_name)
        if category_temp is not None:
            return [subcategory['Name'] for subcategory in self.subcategories if
                    subcategory['Category_id'] == category_temp.get('Category_id')]

    def __find_category_by_id(self, category_id):
        for category_temp in self.categories:
            if category_temp.get('Category_id') == category_id:
                return category_temp
        return None

    def __find_subcategory_by_id(self, subcategory_id):
        for subcategory_temp in self.subcategories:
            if subcategory_temp.get('Subcategory_id') == subcategory_id:
                return subcategory_temp
        return None

    def __find_question_by_id(self, question_id):
        for question_temp in self.questions:
            if question_temp.get('Question_id') == question_id:
                return question_temp
        return None

    def __find_answer_by_id(self, answer_id):
        for answer_temp in self.answers:
            if answer_temp.get('Answer_id') == answer_id:
                return answer_temp
        return None
