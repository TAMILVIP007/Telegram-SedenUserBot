# Copyright (C) 2020-2021 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from time import sleep

from pyrogram.types import ChatPermissions
from sedenbot import BRAIN, HELP, LOGS
from sedenecem.core import edit, extract_args, get_translation, sedenify, send_log


def globals_init():
    try:
        global sql, sql2
        from importlib import import_module

        sql = import_module('sedenecem.sql.gban_sql')
        sql2 = import_module('sedenecem.sql.gmute_sql')
    except Exception as e:
        sql = None
        sql2 = None
        LOGS.warn(get_translation('globalsSqlLog'))
        raise e


globals_init()


@sedenify(pattern='^.gban', compat=False)
def gban_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("banProcess")}`')
    if args:
        try:
            user = client.get_users(args)
        except Exception:
            edit(message, f'`{get_translation("banFailUser")}`')
            return
    elif reply:
        user_id = reply.from_user.id
        user = client.get_users(user_id)
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotBanMyself")}`')
    except BaseException:
        pass

    if user.id in BRAIN:
        return edit(
            message,
            get_translation('brainError', ['`', '**', user.first_name, user.id]),
        )

    try:
        if sql.is_gbanned(user.id):
            return edit(message, f'`{get_translation("alreadyBanned")}`')
        sql.gban(user.id)
        edit(
            message,
            get_translation('gbanResult', ['**', user.first_name, user.id, '`']),
        )
        sleep(1)
        send_log(get_translation('gbanLog', [user.first_name, user.id]))
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.ungban', compat=False)
def ungban_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("unbanProcess")}`')
    if args:
        try:
            user = client.get_users(args)
        except Exception:
            edit(message, f'`{get_translation("banFailUser")}`')
            return
    elif reply:
        user_id = reply.from_user.id
        user = client.get_users(user_id)
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotUnbanMyself")}`')
    except BaseException:
        pass

    try:
        if not sql.is_gbanned(user.id):
            return edit(message, f'`{get_translation("alreadyUnbanned")}`')
        chat_id = message.chat.id
        sql.ungban(user.id)
        client.unban_chat_member(chat_id, user.id)
        edit(
            message,
            get_translation('unbanResult', ['**', user.first_name, user.id, '`']),
        )
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.listgban$')
def gbanlist(message):
    users = sql.gbanned_users()
    if not users:
        return edit(message, f'`{get_translation("listEmpty")}`')
    gban_list = f'**{get_translation("gbannedUsers")}**\n'
    for count, i in enumerate(users, start=1):
        gban_list += f'**{count} -** `{i.sender}`\n'
    return edit(message, gban_list)


@sedenify(incoming=True, outgoing=False, compat=False)
def gban_check(client, message):
    if sql.is_gbanned(message.from_user.id):
        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            client.kick_chat_member(chat_id, user_id)
        except BaseException as e:
            send_log(get_translation('banError', ['`', '**', e]))

    message.continue_propagation()


@sedenify(pattern='^.gmute', compat=False)
def gmute_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("muteProcess")}`')
    if len(args):
        try:
            user = client.get_users(args)
        except Exception:
            edit(message, f'`{get_translation("banFailUser")}`')
            return
    elif reply:
        user_id = reply.from_user.id
        user = client.get_users(user_id)
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotMuteMyself")}`')
    except BaseException:
        pass

    if user.id in BRAIN:
        return edit(
            message,
            get_translation('brainError', ['`', '**', user.first_name, user.id]),
        )

    try:
        if sql2.is_gmuted(user.id):
            return edit(message, f'`{get_translation("alreadyMuted")}`')
        sql2.gmute(user.id)
        edit(
            message,
            get_translation('gmuteResult', ['**', user.first_name, user.id, '`']),
        )
        sleep(1)
        send_log(get_translation('gmuteLog', [user.first_name, user.id]))
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.ungmute', compat=False)
def ungmute_user(client, message):
    args = extract_args(message)
    reply = message.reply_to_message
    edit(message, f'`{get_translation("unmuteProcess")}`')
    if len(args):
        try:
            user = client.get_users(args)
        except Exception:
            edit(message, f'`{get_translation("banFailUser")}`')
            return
    elif reply:
        user_id = reply.from_user.id
        user = client.get_users(user_id)
    else:
        edit(message, f'`{get_translation("banFailUser")}`')
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return edit(message, f'`{get_translation("cannotUnmuteMyself")}`')
    except BaseException:
        pass

    try:
        if not sql2.is_gmuted(user.id):
            return edit(message, f'`{get_translation("alreadyUnmuted")}`')
        sql2.ungmute(user.id)
        edit(
            message,
            get_translation('unmuteResult', ['**', user.first_name, user.id, '`']),
        )
    except Exception as e:
        edit(message, get_translation('banError', ['`', '**', e]))
        return


@sedenify(pattern='^.listgmute$')
def gmutelist(message):
    users = sql2.gmuted_users()
    if not users:
        return edit(message, f'`{get_translation("listEmpty")}`')
    gmute_list = f'**{get_translation("gmutedUsers")}**\n'
    for count, i in enumerate(users, start=1):
        gmute_list += f'**{count} -** `{i.sender}`\n'
    return edit(message, gmute_list)


@sedenify(incoming=True, outgoing=False, compat=False)
def gmute_check(client, message):
    if sql2.is_gmuted(message.from_user.id):
        sleep(0.1)
        message.delete()

        try:
            user_id = message.from_user.id
            chat_id = message.chat.id
            client.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()


HELP.update({'globals': get_translation('globalsInfo')})
