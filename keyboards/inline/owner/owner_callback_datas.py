from aiogram.utils.callback_data import CallbackData

confirm_new_manager_callback = CallbackData("confirm", "action", "user_id")
decline_new_manager_callback = CallbackData("decline", "action", "user_id")

choose_admin_callback = CallbackData('choose_admin', "action", "user_id")
deletion_confirmed_callback = CallbackData("deletion", "action", "user_id")
