import sys

from Service.Service import Service

import tkinter as tk
from tkinter import messagebox


class Controller:
    def __init__(self):
        self.max_score = 0
        self.current_score = 0
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
        # Create a new window
        window = tk.Tk()
        window.title("Create Question")

        # Create and pack the category label and input field
        category_label = tk.Label(window, text="Category:")
        category_label.pack()
        category_entry = tk.Entry(window)
        category_entry.pack()

        # Create and pack the subcategory label and input field
        subcategory_label = tk.Label(window, text="Subcategory:")
        subcategory_label.pack()
        subcategory_entry = tk.Entry(window)
        subcategory_entry.pack()

        # Create and pack the question label and input field
        question_label = tk.Label(window, text="Question:")
        question_label.pack()
        question_entry = tk.Entry(window)
        question_entry.pack()

        # Create and pack the answers label
        answers_label = tk.Label(window, text="Answers:")
        answers_label.pack()

        # Create the answers input fields
        answers_entries = []
        for i in range(4):
            answer_label = tk.Label(window, text=f"Answer {i + 1}:")
            answer_label.pack()
            answer_entry = tk.Entry(window)
            answer_entry.pack()
            answers_entries.append(answer_entry)

        def submit():
            # Get the input values
            category = category_entry.get()
            subcategory = subcategory_entry.get()
            question = question_entry.get()
            answers = [entry.get() for entry in answers_entries]

            # Call the service method to create the question
            self.service.create_question(category, subcategory, question, answers)

            # Show a success message
            messagebox.showinfo("Success", "Question created successfully!")

            # Close the window
            window.destroy()

        # Create and pack the submit button
        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack()

        # Start the Tkinter event loop
        window.mainloop()

    def generate_test(self):
        # Create a new window
        window = tk.Tk()
        window.title("Generate Test")

        # Get the categories from the service
        categories = self.service.get_categories()

        # Create and pack the category label and input field
        category_label = tk.Label(window, text="Category:")
        category_label.pack()
        category_var = tk.StringVar(window)
        category_dropdown = tk.OptionMenu(window, category_var, *categories)
        category_dropdown.pack()

        def on_category_select(*args):
            selected_category = category_var.get()
            subcategories = self.service.get_subcategories(selected_category)

            if not subcategories:
                messagebox.showerror("Error", "No subcategories found for the selected category!")
                return

            # Create and pack the subcategory label and input field
            subcategory_label = tk.Label(window, text="Subcategory:")
            subcategory_label.pack()
            subcategory_var = tk.StringVar(window)
            subcategory_dropdown = tk.OptionMenu(window, subcategory_var, *subcategories)
            subcategory_dropdown.pack()

            def on_generate():
                selected_subcategory = subcategory_var.get()
                num_questions = num_questions_entry.get()
                test = self.service.generate_test(selected_category, selected_subcategory, int(num_questions))

                if test is None:
                    messagebox.showerror("Error",
                                         f"No subcategory '{selected_subcategory}' found in category '{selected_category}'!")
                    return

                # Close the window
                window.destroy()

                # Resolve the test
                self.__resolve_test(test)

            # Create and pack the number of questions label and input field
            num_questions_label = tk.Label(window, text="Number of Questions:")
            num_questions_label.pack()
            num_questions_entry = tk.Entry(window)
            num_questions_entry.pack()

            # Create and pack the generate button
            generate_button = tk.Button(window, text="Generate", command=on_generate)
            generate_button.pack()

        # Bind the category dropdown selection to the callback function
        category_var.trace("w", on_category_select)

        # Start the Tkinter event loop
        self.max_score = 0
        self.current_score = 0
        window.mainloop()

    def delete_category(self):
        # Create a new window
        window = tk.Tk()
        window.title("Delete Category")

        # Get the categories from the service
        categories = self.service.get_categories()

        # Create and pack the category label and input field
        category_label = tk.Label(window, text="Category:")
        category_label.pack()
        category_var = tk.StringVar(window)
        category_dropdown = tk.OptionMenu(window, category_var, *categories)
        category_dropdown.pack()

        def submit():
            selected_category = category_var.get()
            if selected_category not in categories:
                messagebox.showerror("Error", f"No category named '{selected_category}' found!")
                return

            # Call the service method to delete the category
            self.service.delete_category(selected_category)

            # Show a success message
            messagebox.showinfo("Success", "Category deleted successfully!")

            # Close the window
            window.destroy()

        # Create and pack the submit button
        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack()

        # Start the Tkinter event loop
        window.mainloop()

    def delete_subcategory(self):
        # Create a new window
        window = tk.Tk()
        window.title("Delete Subcategory")

        # Get the categories from the service
        categories = self.service.get_categories()

        # Create and pack the category label and input field
        category_label = tk.Label(window, text="Category:")
        category_label.pack()
        category_var = tk.StringVar(window)
        category_dropdown = tk.OptionMenu(window, category_var, *categories)
        category_dropdown.pack()

        def on_category_select(*args):
            selected_category = category_var.get()
            subcategories = self.service.get_subcategories(selected_category)

            if not subcategories:
                messagebox.showerror("Error", "No subcategories found for the selected category!")
                return

            # Create and pack the subcategory label and input field
            subcategory_label = tk.Label(window, text="Subcategory:")
            subcategory_label.pack()
            subcategory_var = tk.StringVar(window)
            subcategory_dropdown = tk.OptionMenu(window, subcategory_var, *subcategories)
            subcategory_dropdown.pack()

            def submit():
                selected_subcategory = subcategory_var.get()

                # Call the service method to delete the subcategory
                self.service.delete_subcategory_by_name(selected_subcategory, selected_category)

                # Show a success message
                messagebox.showinfo("Success", "Subcategory deleted successfully!")

                # Close the window
                window.destroy()

            # Create and pack the submit button
            submit_button = tk.Button(window, text="Submit", command=submit)
            submit_button.pack()

        # Bind the category dropdown selection to the callback function
        category_var.trace("w", on_category_select)

        # Start the Tkinter event loop
        window.mainloop()

    def delete_question(self):
        # Create a new window
        window = tk.Tk()
        window.title("Delete Question")

        # Create and pack the question label and input field
        question_label = tk.Label(window, text="Question:")
        question_label.pack()
        question_entry = tk.Entry(window)
        question_entry.pack()

        def submit():
            question = question_entry.get()

            # Call the service method to delete the question
            self.service.delete_question(question)

            # Show a success message
            messagebox.showinfo("Success", "Question deleted successfully!")

            # Close the window
            window.destroy()

        # Create and pack the submit button
        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack()

        # Start the Tkinter event loop
        window.mainloop()

    def quit_app(self):
        print('Dzieki za skorzystanie z naszej aplikacji!')
        sys.exit(0)

    def __resolve_test(self, test):
        if len(test) > self.max_score:
            self.max_score = len(test)

        # Create a new window for the test resolution
        window = tk.Tk()
        window.title("Test Resolution")

        def submit():
            selected_answer = answer_var.get()
            for answer in question.get('Answers'):
                if answer.get('Is_correct') and selected_answer == str(answer.get('Answer_id')):
                    # Increment the score for correct answers
                    self.current_score += 1
                    break

            # Remove the question and answer widgets
            question_label.pack_forget()
            for widget in window.winfo_children():
                widget.pack_forget()

            # Proceed to the next question or finish the test
            if len(test) > 1:
                resolve_next_question()
            else:
                resolve_final_score()

        def resolve_next_question():
            # Remove the submit button
            submit_button.pack_forget()

            # Proceed to the next question
            test.remove(question)
            self.__resolve_test(test)

        def resolve_final_score():
            # Remove the submit button
            submit_button.pack_forget()

            # Create a label to display the final score
            score_label = tk.Label(window, text=f"Final Score: {self.current_score}/{self.max_score}")
            score_label.pack()

            # Prompt the user to enter their name
            name_label = tk.Label(window, text="Your name:")
            name_label.pack()
            name_entry = tk.Entry(window)
            name_entry.pack()

            def save_score():
                user_name = name_entry.get()
                with open('../scores.txt', 'a') as f:
                    f.write(f'{user_name}: {self.current_score}/{self.max_score}\n')
                window.destroy()

            # Create a button to save the score
            save_button = tk.Button(window, text="Save Score", command=save_score)
            save_button.pack()

        # Iterate over each question in the test
        for question in test:
            # Create a label to display the question
            question_label = tk.Label(window, text=question.get('Question'))
            question_label.pack()

            # Create a variable to store the selected answer
            answer_var = tk.StringVar(window)
            answer_var.set(None)  # Ustawienie początkowej wartości na None

            # Create radio buttons for each answer
            for answer in question.get('Answers'):
                answer_radio = tk.Radiobutton(window, text=answer.get('Answer'), variable=answer_var,
                                              value=answer.get('Answer_id'))
                answer_radio.pack()

            # Create a submit button
            submit_button = tk.Button(window, text="Submit", command=submit)
            submit_button.pack()

            # Break the loop after displaying the first question
            break

        # Start the Tkinter event loop
        window.mainloop()

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
