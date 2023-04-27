from controller import Controller


def print_menu():
    print("1. Dodaj pytanie")
    print("2. Usun kategorie")
    print("3. Usun podkategorie")
    print("4. Usun pytanie")
    print("5. Wygeneruj test")
    print("6. Wyjdz z aplikacji")
    print()


if __name__ == '__main__':
    user_controller = Controller()
    user_controller.fill_data()

    switch = {
        1: user_controller.create_question,
        2: user_controller.delete_category,
        3: user_controller.delete_subcategory,
        4: user_controller.delete_question,
        5: user_controller.generate_test,
        6: user_controller.quit_app
    }

    while True:
        print_menu()
        value = input("Co chcesz zrobic? ")
        try:
            value = int(value)
        except ValueError:
            print("Niepoprawna wartość, spróbuj ponownie.")
            continue

        if value in switch:
            switch[value]()
        else:
            print("Nieznana opcja, spróbuj ponownie.")

# TODO:
# - provide DTOs
# - create DAOs
# - more complex logic
# - create GUI interface
