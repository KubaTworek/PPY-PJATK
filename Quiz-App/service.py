import random


class Service:
    def __init__(self):
        self.questions = []

    def create_question(self, category, subcategory, question, answers):
        question_entity = {
            'category': category,
            'subcategory': subcategory,
            'question': question,
            'answers': answers,
        }
        self.questions.append(question_entity)

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
