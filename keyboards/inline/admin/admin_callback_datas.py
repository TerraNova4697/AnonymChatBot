from aiogram.utils.callback_data import CallbackData

choose_question_callback = CallbackData("question", "action", "question_id")
edit_question_keyboard = CallbackData("edit_question", "action", "question_id")
edit_category_keyboard = CallbackData("edit_category", "action", "category")
delete_question_callback = CallbackData("delete_quest", "action", "question_id")
choose_openness_callback = CallbackData("add_question", "action", "openness")

choose_f_question_callback = CallbackData("question", "action", "f_question_id")
edit_f_question_callback = CallbackData("edit_f_question", "action", "f_question_id")
