import sqlite3


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


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
