from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import types
from tgbot.handlers import user, auth
from tgbot.handlers import admin
from tgbot.keyboards.query_cb import LanguageCallback
from tgbot.misc.states.user import AuthUser, UserState


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin.start.start_handler,
        commands=['start'],
        is_admin=True,
        state="*"
    )


def register_client(dp: Dispatcher):
    dp.register_message_handler(
        user.auth.auth_lang_handler,
        commands=['start'],
        is_auth=False,
        state="*"
    )
    dp.register_callback_query_handler(
        user.auth.auth_name_handler,
        LanguageCallback.filter(action='lang_auth'),
        state=AuthUser.wait_lang
    )

    dp.register_message_handler(
        user.auth.auth_user_handler,
        state=AuthUser.wait_name
    )

    #dp.register_message_handler(
    #    user.auth.auth_phone_handler,
    #    state=AuthUser.wait_name
    #)

    #dp.register_message_handler(
    #    user.auth.auth_user_handler,
    #    content_types=types.ContentType.CONTACT,
    #    state=AuthUser.wait_phone
    #)

    dp.register_message_handler(
        #auth.auth_user_handler,
        user.start.start_handler,
        commands=['start'],
        is_auth=True,
        state='*'
    )

    #dp.register_message_handler(
    #    user.start.start_handler,
    #    content_types=types.ContentType.CONTACT,
    #    state=UserState.wait_user
    #)

