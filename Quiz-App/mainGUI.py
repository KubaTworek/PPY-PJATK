from tkinter import Tk, Button, Label, Entry, Frame, messagebox
from Controller.TkinterController import Controller


class MainGUI:
    def __init__(self):
        self.controller = Controller()
        self.controller.fill_data()

        self.window = Tk()
        self.window.title("Quiz App")

        self.create_widgets()

    def create_widgets(self):
        buttons_frame = Frame(self.window, padx=20, pady=20)
        buttons_frame.pack()

        self.add_question_button = Button(buttons_frame, text="Dodaj pytanie", command=self.controller.create_question, width=30)
        self.add_question_button.pack(pady=10)

        self.delete_category_button = Button(buttons_frame, text="Usuń kategorię", command=self.controller.delete_category, width=30)
        self.delete_category_button.pack(pady=10)

        self.delete_subcategory_button = Button(buttons_frame, text="Usuń podkategorię", command=self.controller.delete_subcategory, width=30)
        self.delete_subcategory_button.pack(pady=10)

        self.delete_question_button = Button(buttons_frame, text="Usuń pytanie", command=self.controller.delete_question, width=30)
        self.delete_question_button.pack(pady=10)

        self.generate_test_button = Button(buttons_frame, text="Wygeneruj test", command=self.controller.generate_test, width=30)
        self.generate_test_button.pack(pady=10)

        self.quit_button = Button(buttons_frame, text="Wyjdź z aplikacji", command=self.controller.quit_app, width=30)
        self.quit_button.pack(pady=10)

    def run(self):
        self.window.update_idletasks()
        window_width = 300
        window_height = 350
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.window.mainloop()


if __name__ == '__main__':
    gui = MainGUI()
    gui.run()
