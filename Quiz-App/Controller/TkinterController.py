import sys
import tkinter as tk
from tkinter import messagebox

from Service.Service import Service


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
        window = tk.Tk()
        window.title("Create Question")

        form_frame = tk.Frame(window)
        form_frame.pack(padx=20, pady=10)

        category_label = tk.Label(form_frame, text="Category:")
        category_label.pack()
        category_entry = tk.Entry(form_frame, width=40)
        category_entry.pack(pady=5)

        subcategory_label = tk.Label(form_frame, text="Subcategory:")
        subcategory_label.pack()
        subcategory_entry = tk.Entry(form_frame, width=40)
        subcategory_entry.pack(pady=5)

        question_label = tk.Label(form_frame, text="Question:")
        question_label.pack()
        question_entry = tk.Entry(form_frame, width=40)
        question_entry.pack(pady=5)

        answers_label = tk.Label(form_frame, text="Answers:")
        answers_label.pack()

        answers_entries = []
        correct_vars = []
        for i in range(4):
            answer_frame = tk.Frame(form_frame)
            answer_frame.pack(pady=5)

            answer_entry = tk.Entry(answer_frame, width=30)
            answer_entry.pack(side=tk.LEFT)
            answers_entries.append(answer_entry)

            correct_var = tk.IntVar()
            correct_check = tk.Checkbutton(answer_frame, text="Correct", variable=correct_var)
            correct_check.pack(side=tk.LEFT)
            correct_vars.append(correct_var)

        def submit():
            category = category_entry.get()
            subcategory = subcategory_entry.get()
            question = question_entry.get()

            answers = []
            for i in range(4):
                content = answers_entries[i].get()
                is_correct = correct_vars[i].get()
                answer = {
                    'content': content,
                    'is_correct': is_correct
                }
                answers.append(answer)

            self.service.create_question(category, subcategory, question, answers)

            messagebox.showinfo("Success", "Question created successfully!")

            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=10)

        center_window(window)

        window.mainloop()

    def generate_test(self):
        window = tk.Tk()
        window.title("Generate Test")

        categories = self.service.get_categories()

        category_label = tk.Label(window, text="Category:")
        category_label.pack(pady=10)
        category_var = tk.StringVar(window)
        category_dropdown = tk.OptionMenu(window, category_var, *categories)
        category_dropdown.pack(pady=5)

        def on_category_select(*args):
            selected_category = category_var.get()
            subcategories = self.service.get_subcategories(selected_category)

            if not subcategories:
                messagebox.showerror("Error", "No subcategories found for the selected category!")
                return

            subcategory_label = tk.Label(window, text="Subcategory:")
            subcategory_label.pack(pady=10)
            subcategory_var = tk.StringVar(window)
            subcategory_dropdown = tk.OptionMenu(window, subcategory_var, *subcategories)
            subcategory_dropdown.pack(pady=5)

            def on_generate():
                selected_subcategory = subcategory_var.get()
                num_questions = num_questions_entry.get()
                test = self.service.generate_test(selected_category, selected_subcategory, int(num_questions))

                if test is None:
                    messagebox.showerror("Error",
                                         f"No subcategory '{selected_subcategory}' found in category '{selected_category}'!")
                    return

                window.destroy()

                self.__resolve_test(test)

            num_questions_label = tk.Label(window, text="Number of Questions:")
            num_questions_label.pack(pady=10)
            num_questions_entry = tk.Entry(window)
            num_questions_entry.pack(pady=5)

            generate_button = tk.Button(window, text="Generate", command=on_generate)
            generate_button.pack(pady=20)

        category_var.trace("w", on_category_select)

        center_window(window)

        window.mainloop()

    def delete_category(self):
        def submit():
            selected_category = category_var.get()
            if selected_category not in categories:
                messagebox.showerror("Error", f"No category named '{selected_category}' found!")
                return

            self.service.delete_category(selected_category)

            messagebox.showinfo("Success", "Category deleted successfully!")

            window.destroy()

        window = tk.Tk()
        window.title("Delete Category")

        categories = self.service.get_categories()

        category_label = tk.Label(window, text="Category:")
        category_label.pack(pady=10)
        category_var = tk.StringVar(window)
        category_dropdown = tk.OptionMenu(window, category_var, *categories)
        category_dropdown.pack(pady=5)

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=20)

        center_window(window)

        window.mainloop()

    def delete_subcategory(self):
        window = tk.Tk()
        window.title("Delete Subcategory")

        categories = self.service.get_categories()

        category_label = tk.Label(window, text="Category:")
        category_label.pack(pady=10)
        category_var = tk.StringVar(window)
        category_dropdown = tk.OptionMenu(window, category_var, *categories)
        category_dropdown.pack(pady=5)

        def on_category_select(*args):
            selected_category = category_var.get()
            subcategories = self.service.get_subcategories(selected_category)

            if not subcategories:
                messagebox.showerror("Error", "No subcategories found for the selected category!")
                return

            subcategory_label = tk.Label(window, text="Subcategory:")
            subcategory_label.pack(pady=10)
            subcategory_var = tk.StringVar(window)
            subcategory_dropdown = tk.OptionMenu(window, subcategory_var, *subcategories)
            subcategory_dropdown.pack(pady=5)

            def submit():
                selected_subcategory = subcategory_var.get()

                self.service.delete_subcategory_by_name(selected_subcategory, selected_category)

                messagebox.showinfo("Success", "Subcategory deleted successfully!")

                window.destroy()

            submit_button = tk.Button(window, text="Submit", command=submit)
            submit_button.pack(pady=20)

        category_var.trace("w", on_category_select)

        center_window(window)

        window.mainloop()

    def delete_question(self):
        def submit():
            question = question_entry.get()

            self.service.delete_question(question)

            messagebox.showinfo("Success", "Question deleted successfully!")

            window.destroy()

        window = tk.Tk()
        window.title("Delete Question")

        question_label = tk.Label(window, text="Question:")
        question_label.pack(pady=10)
        question_entry = tk.Entry(window)
        question_entry.pack(pady=5)

        submit_button = tk.Button(window, text="Submit", command=submit)
        submit_button.pack(pady=20)

        center_window(window)

        window.mainloop()

    def quit_app(self):
        print('Dzieki za skorzystanie z naszej aplikacji!')
        sys.exit(0)

    def __resolve_test(self, test):
        if len(test) > self.max_score:
            self.max_score = len(test)

        window = tk.Tk()
        window.title("Test Resolution")

        def submit():
            selected_answer = answer_var.get()
            for answer in question.get('Answers'):
                if answer.get('Is_correct') and selected_answer == str(answer.get('Answer_id')):
                    self.current_score += 1
                    break

            question_label.pack_forget()
            submit_button.pack_forget()

            test.remove(question)

            if len(test) > 0:
                resolve_next_question()
            else:
                resolve_final_score()

        def resolve_next_question():
            self.__resolve_test(test)

        def resolve_final_score():
            score_label = tk.Label(window, text=f"Final Score: {self.current_score}/{self.max_score}",
                                   font=("Arial", 14, "bold"))
            score_label.pack(pady=10)

            name_label = tk.Label(window, text="Your name:", font=("Arial", 12, "bold"))
            name_label.pack()
            name_entry = tk.Entry(window, font=("Arial", 12, "bold"))
            name_entry.pack()

            def save_score():
                user_name = name_entry.get()
                with open('../scores.txt', 'a') as f:
                    f.write(f'{user_name}: {self.current_score}/{self.max_score}\n')
                window.destroy()

            save_button = tk.Button(window, text="Save Score", command=save_score, font=("Arial", 12, "bold"))
            save_button.pack(pady=10)

        question = test[0]

        question_label = tk.Label(window, text=question.get('Question'), font=("Arial", 12, "bold"))
        question_label.pack(pady=10)

        answer_var = tk.StringVar(window)
        answer_var.set(None)

        for answer in question.get('Answers'):
            answer_radio = tk.Radiobutton(window, text=answer.get('Answer'), variable=answer_var,
                                          value=answer.get('Answer_id'))
            answer_radio.pack()

        submit_button = tk.Button(window, text="Submit", command=submit, font=("Arial", 12, "bold"))
        submit_button.pack(pady=10)

        center_window(window)

        window.mainloop()


def center_window(window):
    window.update_idletasks()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
