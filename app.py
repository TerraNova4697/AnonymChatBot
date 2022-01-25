from aiogram import executor

from data import variables
from data.variables import admins
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Создаем таблицы
    try:
        db.create_table_admins()
    except Exception as err:
        print(err)

    try:
        db.create_table_user()
    except Exception as err:
        print(err)

    try:
        db.create_table_questions()
    except Exception as err:
        print(err)

    try:
        db.create_table_form_questions()
    except Exception as err:
        print(err)
    # db.populate_forms()

    try:
        db.create_table_forms_answers()
    except Exception as err:
        print(err)

    # db.populate_questions()

    # Create tables for test
    try:
        db.create_table_test_questions()
        db.create_table_test_variants()
    except Exception as err:
        print(err)
    # populate test with questions and answers
    # db.populate_test_with_answers()

    # Загружаем списки администраторов
    list_of_managers = db.select_all_admins_user_id(status="Active")
    for user_id in list_of_managers:
        admins.append(user_id[0])
    # Загружаем вопросы и ответы тестов
    list_of_test_questions = db.select_all_test_questions()
    for question in list_of_test_questions:
        list_of_answers = db.select_test_answers(question_id=question[0])
        variables.test[question[1]] = list_of_answers

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
