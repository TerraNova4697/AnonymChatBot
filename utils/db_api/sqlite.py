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

    def create_table_users_filled_forms(self):
        sql = """
        CREATE TABLE UsersFilledForms (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id int NOT NULL,
        f_question_id int NOT NULL,
        f_question_text varchar NOT NULL,
        f_answer_id int,
        is_important varchar(255) NOT NULL,
        partners_value int NOT NULL, 
        partners_text_value varchar NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def create_table_user(self):
        sql = """
        CREATE TABLE Users (
        user_id int NOT NULL,
        name varchar(255),
        status varchar(255) NOT NULL,
        partner_id int NOT NULL,
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

    def create_table_chats(self):
        sql = """
        CREATE TABLE Chats (
        chat_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        partner1_id int NOT NULL,
        partner2_id int NOT NULL,
        openness varchar(255),
        status varchar(255),
        exchange_contacts varchar (255),
        partner1_phone_number varchar(255),
        partner2_phone_number varchar(255),
        answered_questions varchar(255),
        partner1_passed int NOT NULL,
        partner2_passed int NOT NULL,
        partner1_ready_to_lvl_up varchar(255),
        partner2_ready_to_lvl_up varchar(255)
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

    def select_all_active_forms_questions(self):
        sql = "SELECT f_questions_id, text FROM FormsQuestions WHERE status='Active'"
        return self.execute(sql, fetchall=True)

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
        sql = "SELECT text, answer_id FROM FormsAnswers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_f_answer(self, **kwargs):
        sql = "SELECT text, form_question_id, answer_id FROM FormsAnswers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_f_answer_text_by_id(self, **kwargs):
        sql = "SELECT text FROM FormsAnswers WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def insert_new_form_answer(self, form_question_id: int, text: str):
        sql = "INSERT INTO FormsAnswers(form_question_id, text) VALUES (?, ?)"
        self.execute(sql, parameters=(form_question_id, text), commit=True)

    # UsersFormsAnswers operations
    def insert_users_forms_answers_before_test(self, user_id: int, f_question_id, f_question_text, is_important="False",
                                               partners_value=0, partners_text_value: str = ""):
        sql = "INSERT INTO UsersFilledForms(user_id, f_question_id, f_question_text, is_important, " \
              "partners_value, partners_text_value)" \
              " VALUES (?, ?, ?, ?, ?, ?)"
        self.execute(sql, parameters=(user_id, f_question_id, f_question_text, is_important,
                                      partners_value, partners_text_value), commit=True)

    def update_users_filled_forms_with_answer(self, f_question_id: int, user_id: int, f_answer_id: int):
        sql = "UPDATE UsersFilledForms SET f_answer_id=? WHERE f_question_id=? AND user_id=?"
        return self.execute(sql, parameters=(f_answer_id, f_question_id, user_id), commit=True)

    def insert_users_filled_forms(self, user_id: int, f_question_id,
                                  f_question_text, f_answer_id, is_important="False", partners_value=''):
        sql = "INSERT INTO UsersFilledForms(user_id, f_question_id, f_question_text, f_answer_id, is_important, " \
              "partners_value)" \
              " VALUES (?, ?, ?, ?, ?, ?)"
        self.execute(sql, parameters=(user_id, f_question_id, f_question_text, f_answer_id, is_important,
                                      partners_value), commit=True)

    def select_all_users_filled_forms(self, **kwargs):
        sql = "SELECT * FROM UsersFilledForms WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def select_users_filled_form(self, **kwargs):
        sql = "SELECT * FROM UsersFilledForms WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def users_filled_forms_set_importance(self, record_id, is_important):
        sql = "UPDATE UsersFilledForms SET is_important=? WHERE record_id=?"
        self.execute(sql, parameters=(is_important, record_id), commit=True)

    def users_filled_forms_update_partners_value(self, record_id, partners_value, partners_text_value):
        sql = "UPDATE UsersFilledForms SET partners_value=?, partners_text_value=? WHERE record_id=?"
        self.execute(sql, parameters=(partners_value, partners_text_value, record_id), commit=True)

    def drop_table(self):
        sql = "DROP TABLE UsersFilledForms"
        self.execute(sql, commit=True)

    def delete_filled_forms(self):
        sql = "DELETE FROM UsersFilledForms WHERE TRUE"
        self.execute(sql, commit=True)

    def count_all_important_f_questions(self, **kwargs):
        sql = "SELECT COUNT(*) FROM UsersFilledForms WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    # Users table operations
    def add_user(self, user_id: int, status: str = "Inactive", partner_id: int = 0):
        sql = "INSERT INTO Users(user_id, status, partner_id) VALUES (?, ?, ?)"
        self.execute(sql, parameters=(user_id, status, partner_id), commit=True)

    def activate_user(self, user_id: int, status: str):
        sql = "UPDATE Users SET status=? WHERE user_id=?"
        self.execute(sql, parameters=(status, user_id), commit=True)

    def update_users_status_in_search(self, status: str, user_id: int):
        sql = "UPDATE Users SET status=? WHERE user_id=?"
        self.execute(sql, parameters=(status, user_id), commit=True)

    def update_users_status_and_partner_id(self, status: str, partner_id: int, user_id: int):
        sql = "UPDATE Users SET status=?, partner_id=? WHERE user_id=?"
        self.execute(sql, parameters=(status, partner_id, user_id))

    def update_username(self, user_id: int, name: str):
        sql = "UPDATE Users SET name=? WHERE user_id=?"
        self.execute(sql, parameters=(name, user_id), commit=True)

    def select_all_users(self):
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    def select_user_by_id(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_users_in_search(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def delete_users(self):
        sql = "DELETE FROM Users WHERE TRUE"
        self.execute(sql, commit=True)

    def drop_table_users(self):
        sql = "DROP TABLE Users"
        self.execute(sql, commit=True)

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
                # print(list_of_options)
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

    # Chats table operations
    def add_new_chat(self, partner1_id: int, partner2_id: int, openness: str = "", status: str = "OpennessLevel",
                     exchange_contacts: str = "False", partner1_phone_number: str = "",
                     partner2_phone_number: str = "", answered_questions: str = "", partner1_passed: int = 0,
                     partner2_passed: int = 0, partner1_ready_to_lvl_up: str = "False",
                     partner2_ready_to_lvl_up: str = "False"):
        sql = "INSERT INTO Chats(partner1_id, partner2_id, openness, status, exchange_contacts, partner1_phone_number, " \
              "partner2_phone_number, answered_questions, partner1_passed, partner2_passed, partner1_ready_to_lvl_up, " \
              "partner2_ready_to_lvl_up) " \
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.execute(sql, parameters=(partner1_id, partner2_id, openness, status, exchange_contacts,
                                      partner1_phone_number, partner2_phone_number, answered_questions,
                                      partner1_passed, partner2_passed, partner1_ready_to_lvl_up,
                                      partner2_ready_to_lvl_up), commit=True)

    def select_chat_by_partner_id(self, partner1_id: int, partner2_id: int):
        sql = f"SELECT * FROM Chats WHERE partner1_id=? OR partner2_id=?"
        return self.execute(sql, parameters=(partner1_id, partner2_id), fetchone=True)

    def update_chat_openness(self, openness: str, chat_id: int):
        sql = "UPDATE Chats SET openness=? WHERE chat_id=?"
        self.execute(sql, parameters=(openness, chat_id), commit=True)

    def update_chat_status(self, status: str, chat_id: int):
        sql = "UPDATE Chats SET status=? WHERE chat_id=?"
        self.execute(sql, parameters=(status, chat_id), commit=True)

    def drop_table_chats(self):
        sql = "DROP TABLE Chats"
        self.execute(sql, commit=True)

    def update_chat_exchange_contacts_partner1(self, exchange_contacts: str, partner1_phone_number: str, chat_id: int):
        sql = "UPDATE Chats SET exchange_contacts=?, partner1_phone_number=? WHERE chat_id=?"
        self.execute(sql, parameters=(exchange_contacts, partner1_phone_number, chat_id), commit=True)

    def update_chat_exchange_contacts_partner2(self, exchange_contacts: str, partner2_phone_number: str, chat_id: int):
        sql = "UPDATE Chats SET exchange_contacts=?, partner2_phone_number=? WHERE chat_id=?"
        self.execute(sql, parameters=(exchange_contacts, partner2_phone_number, chat_id), commit=True)

    def update_chats_answered_questions(self, answered_questions, chat_id):
        sql = "UPDATE Chats SET answered_questions=? WHERE chat_id=?"
        self.execute(sql, parameters=(answered_questions, chat_id), commit=True)

    def update_partner1_passed_questions(self, partner1_passed, chat_id):
        sql = "UPDATE Chats SET partner1_passed=? WHERE chat_id=?"
        self.execute(sql, parameters=(partner1_passed, chat_id), commit=True)

    def update_partner2_passed_questions(self, partner2_passed, chat_id):
        sql = "UPDATE Chats SET partner2_passed=? WHERE chat_id=?"
        self.execute(sql, parameters=(partner2_passed, chat_id), commit=True)

    def update_partner1_and_2_passed_questions(self, partner1_passed, partner2_passed, chat_id):
        sql = "UPDATE Chats SET partner1_passed=?, partner2_passed=? WHERE chat_id=?"
        self.execute(sql, parameters=(partner1_passed, partner2_passed, chat_id), commit=True)

    def update_chat_partner1_ready_to_lvl_up(self, partner1_ready_to_lvl_up, chat_id):
        sql = "UPDATE Chats SET partner1_ready_to_lvl_up=? WHERE chat_id=?"
        self.execute(sql, parameters=(partner1_ready_to_lvl_up, chat_id), commit=True)

    def update_chat_partner2_ready_to_lvl_up(self, partner2_ready_to_lvl_up, chat_id):
        sql = "UPDATE Chats SET partner2_ready_to_lvl_up=? WHERE chat_id=?"
        self.execute(sql, parameters=(partner2_ready_to_lvl_up, chat_id), commit=True)

    def update_chat_openness_and_readiness(self, openness, partner1_ready_to_lvl_up, partner2_ready_to_lvl_up,
                                           partner1_passed, partner2_passed, chat_id):
        sql = "UPDATE Chats SET openness=?, partner1_ready_to_lvl_up=?, partner2_ready_to_lvl_up=?, partner1_passed=?," \
              "partner2_passed=? WHERE chat_id=?"
        self.execute(sql, parameters=(openness, partner1_ready_to_lvl_up, partner2_ready_to_lvl_up,
                                      partner1_passed, partner2_passed, chat_id), commit=True)

    def delete_chat_by_partner_id(self, partner1_id, partner2_id):
        sql = "DELETE FROM Chats WHERE partner1_id=? OR partner2_id=?"
        self.execute(sql, parameters=(partner1_id, partner2_id), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
