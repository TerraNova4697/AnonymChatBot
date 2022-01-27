import sqlite3

from data import variables


class Database:
    def __init__(self, path_to_db='main.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()

        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # TABLES
    def create_table_admins(self):
        sql = """
        CREATE TABLE Admins (
        user_id int NOT NULL,
        name varchar(255) NOT NULL,
        surname varchar(255) NOT NULL,
        status varchar NOT NULL,
        email varchar(255) NOT NULL,
        PRIMARY KEY (user_id)
        );
        """
        self.execute(sql, commit=True)

    def create_table_questions(self):
        sql = """
        CREATE TABLE Questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        question varchar(300) NOT NULL,
        category varchar(255) NOT NULL,
        openness varchar(255) NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def create_table_form_questions(self):
        sql = """
        CREATE TABLE FormsQuestions (
        f_questions_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        text varchar(255) NOT NULL,
        status varchar(255) NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def create_table_forms_answers(self):
        sql = """
        CREATE TABLE FormsAnswers (
        answer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
        form_question_id int NOT NULL,
        text varchar(255) NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def create_table_user(self):
        sql = """
        CREATE TABLE Users (
        user_id int NOT NULL,
        name varchar(255),
        status varchar(255) NOT NULL,
        PRIMARY KEY (user_id)
        );
        """
        self.execute(sql, commit=True)

    def create_table_quiz_questions(self):
        sql = """
        CREATE TABLE QuizQuestions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id int NOT NULL,
        question varchar NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def create_table_test_questions(self):
        sql = """
        CREATE TABLE TestQuestions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        question_text varchar NOT NULL,
        is_active varchar(255) NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def create_table_test_variants(self):
        sql = """
        CREATE TABLE TestAnswers (
        answer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        answer_text varchar NOT NULL,
        is_true varchar(255) NOT NULL,
        question_id int NOT NULL
        );
        """
        self.execute(sql, commit=True)

    # STRINGS FORMATTING
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item}=?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    # Admin table operations
    def add_admin(self, user_id: int, name: str, surname: str, status: str = "Inactive", email: str = ''):
        sql = "INSERT INTO Admins(user_id, name, surname, status, email) VALUES(?, ?, ?, ?, ?)"
        self.execute(sql, parameters=(user_id, name, surname, status, email), commit=True)

    def update_admin(self, user_id: int, status: str):
        sql = f"""
                UPDATE Admins SET status=? WHERE user_id=?
                """
        return self.execute(sql, parameters=(status, user_id), commit=True)

    def select_admin_by_user_id(self, **kwargs):
        sql = "SELECT name, surname FROM Admins WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_admins_user_id(self, **kwargs):
        sql = "SELECT user_id, email FROM Admins WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_all_active_admins(self, **kwargs):
        sql = "SELECT * FROM Admins WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def inactivate_admin(self, user_id: int, status: str):
        sql = "UPDATE Admins SET status=? WHERE user_id=?"
        return self.execute(sql, parameters=(status, user_id), commit=True)

    # Questions table operations
    def add_question(self, question: str, category: str, openness: str):
        sql = "INSERT INTO Questions(question, category, openness) VALUES (?, ?, ?)"
        self.execute(sql, parameters=(question, category, openness), commit=True)

    def populate_questions(self):
        questions = ['Это первый вопрос?', "Это второй вопрос?", "Это третий вопрос?", "Это четвертый вопрос?",
                     "Это пятый вопрос?"]
        category = ['Музыка', "Кино", "Путешествия", "Музыка", "Шопинг"]
        openness = ["Формальный", "Приятельский", "Дружеский", "Близость", "Исповедь"]
        for ind, question in enumerate(questions):
            self.add_question(question=questions[ind], category=category[ind], openness=openness[ind])

    def select_all_questions(self):
        sql = "SELECT * FROM Questions"
        return self.execute(sql, fetchall=True)

    def select_question(self, **kwargs):
        sql = "SELECT * FROM Questions WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def update_questions_text(self, question: str, question_id: int):
        sql = "UPDATE Questions SET question=? WHERE question_id=?"
        return self.execute(sql, parameters=(question, question_id), commit=True)

    def select_all_question_categories(self):
        sql = "SELECT DISTINCT category from Questions WHERE category NOT LIKE 'Без категории%'"
        return self.execute(sql, fetchall=True)

    def update_questions_category(self, category: str, question_id: int):
        sql = "UPDATE Questions SET category=? WHERE question_id=?"
        return self.execute(sql, parameters=(category, question_id), commit=True)

    def update_questions_openness(self, openness: str, question_id: int):
        sql = "UPDATE Questions SET openness=? WHERE question_id=?"
        return self.execute(sql, parameters=(openness, question_id), commit=True)

    def delete_question(self, question_id: int):
        sql = "DELETE FROM Questions WHERE question_id=?"
        return self.execute(sql, parameters=(question_id,), commit=True)

    # Forms operations
    def add_forms_question(self, text, status="Inactive"):
        sql = "INSERT INTO FormsQuestions(text, status) VALUES (?, ?)"
        self.execute(sql, parameters=(text, status), commit=True)

    def select_f_question_form(self, **kwargs):
        sql = "SELECT * FROM FormsQuestions WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_forms_questions(self):
        sql = "SELECT * FROM FormsQuestions"
        return self.execute(sql, fetchall=True)

    def activate_f_question(self, f_questions_id: int, status="Active"):
        sql = "UPDATE FormsQuestions SET status=? WHERE f_questions_id=?"
        return self.execute(sql, parameters=(status, f_questions_id), commit=True)

    def populate_forms(self):
        questions_list = ['Семейное положение', "Отношение к гороскопу", "Домашние животные", "Характер темперамент",
                          "Религия", "Музыка", "Видеоигры"]
        for question in questions_list:
            print(question)
            self.add_forms_question(question)

    def delete_f_question(self, f_questions_id: int):
        sql = "DELETE FROM FormsQuestions WHERE f_questions_id=?"
        return self.execute(sql, parameters=(f_questions_id,), commit=True)

    # FormsAnswers operations
    def select_all_f_answers(self, **kwargs):
        sql = "SELECT text FROM FormsAnswers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def insert_new_form_answer(self, form_question_id: int, text: str):
        sql = "INSERT INTO FormsAnswers(form_question_id, text) VALUES (?, ?)"
        self.execute(sql, parameters=(form_question_id, text), commit=True)

    # Users table operations
    def add_user(self, user_id: int, status: str = "Inactive"):
        sql = "INSERT INTO Users(user_id, status) VALUES (?, ?)"
        self.execute(sql, parameters=(user_id, status), commit=True)

    def activate_user(self, user_id: int, status: str):
        sql = "UPDATE Users SET status=? WHERE user_id=?"
        self.execute(sql, parameters=(status, user_id), commit=True)

    # TestQuestions table operations
    def add_question_into_test_questions(self, question_text: str, is_active="False"):
        sql = "INSERT INTO TestQuestions(question_text, is_active) VALUES (?, ?)"
        self.execute(sql, parameters=(question_text, is_active,), commit=True)

    def select_all_test_questions(self):
        sql = "SELECT * FROM TestQuestions WHERE is_active='True'"
        return self.execute(sql, fetchall=True)

    def select_test_question_id(self, **kwargs):
        sql = "SELECT question_id FROM TestQuestions WHERE "
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def select_test_question_text(self, **kwargs):
        sql = "SELECT question_text FROM TestQuestions WHERE "
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def select_test_question(self, **kwargs):
        sql = "SELECT * FROM TestQuestions WHERE "
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def activate_test_question(self, question_id: int, is_active="True"):
        sql = "UPDATE TestQuestions SET is_active=? WHERE question_id=?"
        self.execute(sql, parameters=(is_active, question_id), commit=True)

    def update_test_question_text(self, question_id: int, question_text: str):
        sql = "UPDATE TestQuestions SET question_text=? WHERE question_id=?"
        self.execute(sql, parameters=(question_text, question_id), commit=True)

    def delete_test_question(self, question_id: int):
        sql = "DELETE FROM TestQuestions WHERE question_id=?"
        return self.execute(sql, parameters=(question_id,), commit=True)

    def populate_test_with_answers(self):
        try:
            for question in variables.test2.keys():
                self.add_question_into_test_questions(question_text=question, is_active="True")
                curr_question = self.select_test_question(question_text=question)
                list_of_options = variables.test2[curr_question[1]]
                print(list_of_options)
                for option in list_of_options:
                    print(option)
                    self.add_test_option(answer_text=option[0], is_true=option[1], question_id=curr_question[0])
        except Exception as err:
            print(err)

    # TestOptions table operations
    def add_test_option(self, answer_text: str, is_true: str, question_id: int):
        sql = "INSERT INTO TestAnswers(answer_text, is_true, question_id) VALUES (?, ?, ?)"
        self.execute(sql, parameters=(answer_text, is_true, question_id), commit=True)

    def select_test_answers(self, **kwargs):
        sql = "SELECT answer_text, is_true, question_id FROM TestAnswers WHERE "
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def select_all_test_answers(self, **kwargs):
        sql = "SELECT * FROM TestAnswers WHERE "
        sql, parameters = self.format_args(sql=sql, parameters=kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def delete_question_option(self, question_id: int):
        sql = "DELETE FROM TestAnswers WHERE question_id=?"
        return self.execute(sql, parameters=(question_id,), commit=True)

    def delete_option(self, answer_id: int):
        sql = "DELETE FROM TestAnswers WHERE answer_id=?"
        return self.execute(sql, parameters=(answer_id,), commit=True)

    def update_options_text(self, answer_id: int, answer_text: str):
        sql = "UPDATE TestAnswers SET answer_text=? WHERE answer_id=?"
        self.execute(sql, parameters=(answer_text, answer_id), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
