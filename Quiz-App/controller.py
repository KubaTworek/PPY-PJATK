from service import Service


class Controller:
    def __init__(self):
        self.service = Service()

    def fill_data(self):
        data = [
            ("History", "Ancient Civilizations",
             "Which ancient civilization is known for building the Great Pyramid of Giza?",
             ["Rome", "Athens", "Constantinople", "Alexandria"]),
            ("History", "Ancient Civilizations",
             "What is the name of the ancient civilization that developed the first writing system?",
             ["Egypt", "Greece", "Rome", "Persia"]),
            ("History", "Ancient Civilizations", "What was the capital of the Roman Empire?",
             ["Sumerians", "Mayans", "Aztecs", "Incas"]),
            ("History", "Ancient Civilizations", "Who was the first emperor of China?",
             ["Qin Shi Huang", "Han Wudi", "Tang Taizong", "Song Huizong"]),
            ("Science", "Biology",
             "What is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll?",
             ["Photosynthesis", "Respiration", "Digestion", "Fermentation"]),
            ("Science", "Biology", "What is the largest organ in the human body?", ["Skin", "Heart", "Liver", "Brain"]),
            ("Science", "Biology",
             "What is the name of the fluid that transports oxygen and nutrients to cells in the human body?",
             ["Blood", "Lymph", "Saliva", "Semen"]),
            ("Science", "Biology",
             "What is the name of the organelle that is responsible for protein synthesis in cells?",
             ["Ribosome", "Mitochondrion", "Golgi Apparatus", "Endoplasmic Reticulum"]),
            (
            "Science", "Biology", "What is the process by which a single cell divides into two or more daughter cells?",
            ["Cell Division", "Mitosis", "Meiosis", "Binary Fission"]),
            ("Geography", "Capitals", "What is the capital of France?", ["Paris", "Madrid", "Berlin", "Rome"]),
            ("Geography", "Capitals", "What is the capital of Brazil?",
             ["Brasília", "Rio de Janeiro", "São Paulo", "Belo Horizonte"]),
            ("Geography", "Capitals", "What is the capital of Japan?", ["Tokyo", "Seoul", "Beijing", "Taipei"]),
            ("Geography", "Capitals", "What is the capital of Canada?", ["Ottawa", "Toronto", "Montreal", "Vancouver"]),
            ("Geography", "Capitals", "What is the capital of Australia?",
             ["Canberra", "Sydney", "Melbourne", "Brisbane"]),
        ]
        for category, subcategory, question, answers in data:
            self.service.create_question(category, subcategory, question, answers)

    def create_question(self):
        answers = []
        self.__print_properties(self.service.get_categories(), "kategorie")
        category = input("Podaj kategorie: ")
        self.__print_properties(self.service.get_subcategories(), "podkategorie")
        subcategory = input("Podaj podkategorie: ")
        question = input("Podaj pytanie: ")
        for i in range(4):
            answer = input("Podaj odpowiedz: ")
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
        self.__print_properties(self.service.get_subcategories(), "podkategorie")
        name = input("Podaj nazwe: ")
        self.service.delete_subcategory(name)

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
