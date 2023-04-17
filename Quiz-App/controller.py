from service import Service


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

        self.service.create_question('Informatyka', 'Programowanie', 'Co oznacza skrót "OOP"?', [
            {'content': 'Object-Oriented Programming', 'is_correct': True},
            {'content': 'Object-Oriented Protocol', 'is_correct': False},
            {'content': 'Object-Oriented Procedure', 'is_correct': False},
            {'content': 'Object-Oriented Practice', 'is_correct': False},
        ])

    def create_question(self):
        answers = []
        self.__print_properties(self.service.get_categories(), "kategorie")
        category = input("Podaj kategorie: ")
        self.__print_properties(self.service.get_subcategories(category), "podkategorie")
        subcategory = input("Podaj podkategorie: ")
        question = input("Podaj pytanie: ")
        for i in range(4):
            content = input("Podaj odpowiedz: ")
            is_correct_user = input("Czy prawidlowa? (T/F)")
            is_correct = is_correct_user == 'T'
            answer = {
                'content': content,
                'is_correct': is_correct
            }
            answers.append(answer)

        self.service.create_question(category, subcategory, question, answers)

    def generate_test(self):
        self.__print_properties(self.service.get_categories(), "kategorie")
        category = input("Podaj kategorie: ")
        self.__print_properties(self.service.get_subcategories(category), "podkategorie")
        subcategory = input("Podaj podkategorie: ")
        num_questions = int(input("Podaj ilosc pytan: "))
        print(self.service.generate_test(category, subcategory, num_questions))

    def delete_category(self):
        self.__print_properties(self.service.get_categories(), "kategorie")
        name = input("Podaj nazwe: ")
        self.service.delete_category(name)

    def delete_subcategory(self):
        self.__print_properties(self.service.get_categories(), "kategorie")
        category_name = input("Podaj nazwe kategorii: ")
        self.__print_properties(self.service.get_subcategories(category_name), "podkategorie")
        subcategory_name = input("Podaj nazwe podkategorii: ")
        self.service.delete_subcategory_by_name(subcategory_name, category_name)

    def delete_question(self):
        name = input("Podaj nazwe: ")
        self.service.delete_question(name)

    def __print_properties(self, properties, name):
        print()
        if not properties:
            print(f"Brak {name}")
        else:
            print(f"Aktualne {name}:")
            for i, property_temp in enumerate(properties, start=1):
                print(f"{i}. {property_temp}")
