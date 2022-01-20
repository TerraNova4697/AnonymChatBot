from aiogram import executor

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

    # Загружаем списки администраторов
    list_of_managers = db.select_all_admins_user_id(status="Active")
    for user_id in list_of_managers:
        admins.append(user_id[0])

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

