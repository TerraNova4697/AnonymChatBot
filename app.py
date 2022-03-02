from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import variables
from data.variables import admins
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.misc.partner_search.find_partners import find_partner
from utils.misc.user import User
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
        # db.drop_table_users()
        db.create_table_user()
    except Exception as err:
        print(err)

    try:
        db.create_table_questions()
    except Exception as err:
        print(err)

    try:
        # db.drop_table()
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

    try:
        # db.drop_table()
        db.create_table_users_filled_forms()
    except Exception as err:
        print(err)

    # Загружаем списки администраторов
    list_of_managers = db.select_all_admins_user_id(status="Active")
    for user_id in list_of_managers:
        admins.append(user_id[0])
    # Загружаем вопросы и ответы тестов
    list_of_test_questions = db.select_all_test_questions()
    for question in list_of_test_questions:
        list_of_answers = db.select_test_answers(question_id=question[0])
        variables.test[question[1]] = list_of_answers

    # Загружаем анкету
    list_of_forms_questions = db.select_all_active_forms_questions()
    for f_question in list_of_forms_questions:
        list_of_f_answers = db.select_all_f_answers(form_question_id=f_question[0])
        variables.f_questions[f_question[1]] = list_of_f_answers

    users_in_search = db.select_all_users_in_search(status="InSearch")
    for user in users_in_search:
        new_user_to_queue = User()
        new_user_to_queue.user_id = user[0]
        new_user_to_queue.name = user[1]
        new_user_to_queue.status = user[2]
        variables.users_search_queue.append(new_user_to_queue)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(find_partner, "interval", seconds=300, args=(bot, ))
    scheduler.start()

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
