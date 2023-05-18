import sys

from SqlServerService import Service


class Controller:
    def __init__(self):
        self.service = Service()

    def fill_data(self):
        self.service.create_question('Matematyka', 'Algebra', 'Jakie jest rozwiązanie równania x^2 = 4?', [
            {'content': 'x = 2', 'is_correct': True},
            {'content': 'x = -2', 'is_correct': True},
            {'content': 'x = 4', 'is_correct': False},
            {'content': 'x = -4', 'is_correct': False},
        ])

        self.service.create_question('Matematyka', 'Geometria', 'Jak obliczyć pole koła o promieniu 5?', [
            {'content': 'P = 5 * pi', 'is_correct': False},
            {'content': 'P = 25 * pi', 'is_correct': True},
            {'content': 'P = 10 * pi', 'is_correct': False},
            {'content': 'P = 50 * pi', 'is_correct': False},
        ])

        self.service.create_question('Matematyka', 'Geometria', 'Jak obliczyć pole koła o promieniu 4?', [
            {'content': 'P = 4 * pi', 'is_correct': False},
            {'content': 'P = 16 * pi', 'is_correct': True},
            {'content': 'P = 10 * pi', 'is_correct': False},
            {'content': 'P = 50 * pi', 'is_correct': False},
        ])

        self.service.create_question('Informatyka', 'Programowanie', 'Co oznacza skrót "OOP"?', [
            {'content': 'Object-Oriented Programming', 'is_correct': True},
            {'content': 'Object-Oriented Protocol', 'is_correct': False},
            {'content': 'Object-Oriented Procedure', 'is_correct': False},
            {'content': 'Object-Oriented Practice', 'is_correct': False},
        ])

    def create_question(self):
        categories = self.service.get_categories()
        category = self.__get_user_input_with_properties(categories, "kategorie", "Podaj kategorie: ")
        subcategories = self.service.get_subcategories(category)
        subcategory = self.__get_user_input_with_properties(subcategories, "podakategorie", "Podaj podkategorie: ")
        question = self.__get_user_input("Podaj pytanie: ")
        answers = self.__create_answers()
        self.service.create_question(category, subcategory, question, answers)

    def generate_test(self):
        categories = self.service.get_categories()
        category = self.__get_user_input_with_properties(categories, "kategorie", "Podaj kategorie: ")
        subcategories = self.service.get_subcategories(category)

        if not subcategories:
            print('Nie ma takiej kategorii!\n')
            return 0
        subcategory = self.__get_user_input_with_properties(subcategories, "podakategorie", "Podaj podkategorie: ")
        num_questions = self.__get_user_input_int("Podaj ilosc pytan: ")
        test = self.service.generate_test(category, subcategory, num_questions)

        if test is None:
            print(f'Nie ma takiej podkategorii "{subcategory}" w kategorii "{category}"!\n')
            return 0
        self.__resolve_test(test)

    def delete_category(self):
        categories = self.service.get_categories()
        name = self.__get_user_input_with_properties(categories, "kategorie", "Podaj nazwe: ")

        if name not in categories:
            print(f"Nie ma kategorii o nazwie {name}.\n")
            return

        self.service.delete_category(name)

    def delete_subcategory(self):
        categories = self.service.get_categories()
        category_name = self.__get_user_input_with_properties(categories, "kategorie", "Podaj nazwe kategorii: ")
        subcategories = self.service.get_subcategories(category_name)
        subcategory_name = self.__get_user_input_with_properties(subcategories, "podkategorie", "Podaj nazwe subkategorii: ")
        self.service.delete_subcategory_by_name(subcategory_name, category_name)

    def delete_question(self):
        name = self.__get_user_input("Podaj nazwe: ")
        self.service.delete_question(name)

    def quit_app(self):
        print('Dzieki za skorzystanie z naszej aplikacji!')
        sys.exit(0)

    def __create_answers(self):
        answers = []
        for i in range(4):
            content = self.__get_user_input("Podaj odpowiedz: ")
            is_correct_user = self.__get_user_input("Czy prawidlowa? (T/F)")
            is_correct = is_correct_user.lower() == 't'
            answer = {
                'content': content,
                'is_correct': is_correct
            }
            answers.append(answer)
        return answers

    def __resolve_test(self, test):
        score = 0
        for question in test:
            self.__print_question(question)
            if self.__is_answer_correct(question):
                print('Correct!\n')
                score += 1
            else:
                print('Incorrect!\n')
        user_name = self.__get_user_input('Your name: ')
        with open('scores.txt', 'a') as f:
            f.write(f'{user_name}: {score}\n')

    def __print_question(self, question):
        print(question.get('Question'))
        for answer in question.get('Answers'):
            print(str(answer.get('Answer_id')) + '. ' + str(answer.get('Answer')))

    def __is_answer_correct(self, question):
        user_answer = input('Your answer: ')
        for answer in question.get('Answers'):
            if answer.get('Is_correct') and user_answer == str(answer.get('Answer_id')):
                return True
        return False

    def __print_properties(self, properties, name):
        print()
        if not properties:
            print(f"Brak {name}")
        else:
            print(f"Aktualne {name}:")
            for i, property_temp in enumerate(properties, start=1):
                print(f"{i}. {property_temp}")

    def __get_user_input(self, prompt: str) -> str:
        return input(prompt)

    def __get_user_input_with_properties(self, properties, name, prompt: str) -> str:
        self.__print_properties(properties, name)
        return input(prompt)

    def __get_user_input_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Podaj poprawną wartość liczbową.")
