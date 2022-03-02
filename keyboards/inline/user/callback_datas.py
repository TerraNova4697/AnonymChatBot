from aiogram.utils.callback_data import CallbackData

quiz_callback = CallbackData("quiz", "action", "is_true")
forms_callback = CallbackData("forms", "action", "f_ans_id")
forms_importance_callback = CallbackData("importance", "action", "record_id")
important_f_questions_callback = CallbackData("imp_f_quest", "action", "record_id", "f_questions_id")
set_value_callback = CallbackData("set_value", "action", "f_answer_id")
partner_found_callback = CallbackData("found", "action", "partners_id")
