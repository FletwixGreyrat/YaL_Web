import asyncio
import aiogram
import html
import aiosqlite
import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from FSMclasses import *
from keyboards import *
from random import choice

admins = ['820436613', '5722409799','860394447', '5419493305']

botname = 'f_sanonbot'
storage = MemoryStorage()
proxy_url = 'http://proxy.server:3128'
sometoken = '6316567212:AAHPfDJwkQsLnkViYT6a0Aasy6nGVH2LC1A'
maintoken = '6154514452:AAELkAMibEKW3fFRf04IeX61TWIEGIY5dgI'
bot: Bot = Bot(token=maintoken)
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)
commandsList = ['/start', '/setgreet', '/stat', '/setname', '/hide']


def sendlink(link):
    return f"""🎭Анонимные сообщения Telegram.

Ваша персональная ссылка:
👉🏻 {link} 👈🏻

Просто размести эту ссылку в любых соц. сетях и начни получать сообщения 💬"""


@dp.message_handler(commands=['start'], state=None)
async def StartCMD(message: types.Message, state: FSMContext):
    try:
        db = await aiosqlite.connect('data.db')
        lstmes = message.text.split()
        user = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
        user = await user.fetchone()
        if user is None:
            userBot = id(message.from_user.id)
            result = await db.execute("SELECT number FROM users ORDER BY number DESC LIMIT 1")
            result = await result.fetchone()
            currentDatetime = datetime.datetime.now().strftime("%d.%m,%Y")
            await db.execute(
                f"INSERT INTO users (userId, userBot, messages, answers, mygreet, number, amountMessages, amountAnswers, date) VALUES ('{message.from_user.id}', '{userBot}', 0, 0, 'default', {result[0] + 1}, 0, 0, '{currentDatetime}')")
            await db.commit()
        user = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
        user = await user.fetchone()
        link = f'https://t.me/{botname}?start={user[1]}'
        if lstmes[-1] == user[1]:
            await message.answer(sendlink(link), parse_mode='html')
            return
        if len(lstmes) == 2:

            to_user = await db.execute(f'SELECT * FROM users WHERE userBot="{lstmes[-1]}"')
            to_user = await to_user.fetchone()

            if to_user is None:
                await message.answer("Такого пользователя нет. Возможно, он сменил ссылку")
                return
        
            await sendAnonimMessage.message.set()
            async with state.proxy() as data:
                data['to'] = lstmes[-1]
                data['msg'] = 'fromlink'
            await message.answer("""💫 Вы можете отправить анонимное сообщение человеку, по ссылке которого перешли.

Напишите ему сообщение, он сразу же узнает об этом, но не будет знать отправителя. Это анонимно🎭.

Ни в чём себе не отказывайте!
                                 
❤️ Спасибо, что пользуетесь нашим ботом)""", reply_markup=kb1(message.from_user.id))
            link = f'https://t.me/{botname}?start={user[1]}</code>'
        
            if not to_user[4] == 'default':
                await message.answer(to_user[4])
            return
        await db.commit()
        user = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
        user = await user.fetchone()
        link = f'https://t.me/{botname}?start={user[1]}'
        await message.answer(sendlink(link), parse_mode='html')
        await db.close()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')


@dp.callback_query_handler(text_startswith='otmena', state=sendAnonimMessage.message)
async def OtmenaCMD(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.finish()
        db = await aiosqlite.connect('data.db')
        data = call.data.split(':')
        user = await db.execute(f'SELECT * FROM users WHERE userId={data[1]}')
        user = await user.fetchone()
        link = f'https://t.me/{botname}?start={user[1]}'
        await call.message.edit_text(sendlink(link), parse_mode='html')
        await db.close()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {call.from_user.id}    {call.from_user.first_name}')

@dp.message_handler(content_types=['any'], state=sendAnonimMessage.message)
async def MessageCMD(message: types.Message, state: FSMContext):
    if message.text in commandsList:
        await message.delete()
        return
    try:
        db = await aiosqlite.connect('data.db')
        user = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
        user = await user.fetchone()

        await db.execute(f"UPDATE users SET messages={user[2] + 1} WHERE userId='{message.from_user.id}'")
        await db.commit()

        userName = f'<a href="tg://user?id={html.escape(str(message.from_user.id))}">{html.escape(message.from_user.first_name)}</a>'
        if message.from_user.username is None:
            message.from_user.username = 'отсутствует'
        if message.from_user.last_name is None:
            message.from_user.last_name = 'отсутсвует'

        async with state.proxy() as data:
            odmen = await db.execute(f"SELECT * FROM users WHERE userBot='{data['to']}'")
            odmen = await odmen.fetchone()
            personal_admin = await bot.get_chat(odmen[0])
            to_admin = f'Персональная админ панель {personal_admin.first_name}\nИмя: {userName} \nФамилия: {html.escape(message.from_user.last_name)}\nАйди: {message.from_user.id}\nИмя пользователя: @{message.from_user.username}\nОпа) У тебя новое анонимное сообщение, скорей смотри что там🤫\n\n'

            to_user = await db.execute(f'SELECT * FROM users WHERE userBot="{data["to"]}"')
            to_user = await to_user.fetchone()

            if to_user is None:
                msg = await message.answer("Ошибка! Данный пользователь не найден. Это обусловлено двумя причинами:\n1.Вы перешли по неправильной ссылке.\n2.Адресат сменил имя пользоваьтеля.")
                await asyncio.sleep(5)
                await message.delete()
                await state.finish()
                return

            zxc = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
            zxc = await zxc.fetchone()

            if message.photo:
                if to_user[0] in admins:
                    if message.caption is None:
                        message.caption = ''
                    await bot.send_photo(to_user[0], photo=message.photo[-1].file_id,
                                     caption=to_admin + html.escape(message.caption), parse_mode=types.ParseMode.HTML,
                                     reply_markup=answerkb(zxc[5]))
                else:
                    if message.caption is None:
                        message.caption = ''
                    await bot.send_photo(to_user[0], photo=message.photo[-1].file_id,
                                     caption='Опа) У тебя новое анонимное сообщение, скорей смотри что там🤫\n\n' + html.escape(message.caption),
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=answerkb(zxc[5]))
            if message.text:
                if to_user[0] in admins:
                    await bot.send_message(to_user[0], text=to_admin + html.escape(message.text), parse_mode=types.ParseMode.HTML,
                                       reply_markup=answerkb(zxc[5]))
                else:
                    await bot.send_message(to_user[0], text='Опа) У тебя новое анонимное сообщение, скорей смотри что там🤫\n\n' + html.escape(message.text), parse_mode=types.ParseMode.HTML,
                                       reply_markup=answerkb(zxc[5]))
            if message.video:
                if to_user[0] in admins:
                    if message.caption is None:
                        message.caption = ''
                    await bot.send_video(to_user[0], video=message.video.file_id, caption=to_admin + html.escape(message.caption),
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=answerkb(zxc[5]))
                else:
                    if message.caption is None:
                        message.caption = ''
                    await bot.send_video(to_user[0], video=message.video.file_id,
                                     caption='Опа) У тебя новое анонимное сообщение, скорей смотри что там🤫\n\n' + html.escape(message.caption),
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=answerkb(zxc[5]))
            if message.sticker:
                if to_user[0] in admins:
                    await bot.send_message(to_user[0], to_admin, parse_mode=types.ParseMode.HTML)
                else:
                    await bot.send_message(to_user[0], 'Опа) У тебя новое анонимное сообщение, скорей смотри что там🤫\n\n')
                await bot.send_sticker(to_user[0], sticker=message.sticker.file_id,
                                   reply_markup=answerkb(zxc[5]))
            await message.answer('Всё супер, сообщение отправлено', reply_markup=againkb(to_user[5]))

            user = await db.execute(f"SELECT * FROM users WHERE userId={message.from_user.id}")
            user = await user.fetchone()
            currentDatetime = datetime.datetime.now().strftime("%d.%m,%Y")


            if currentDatetime == user[8]:
                await db.execute(f"UPDATE users SET amountMessages={user[6] + 1} WHERE userBot='{user[1]}'")
            else:
                await db.execute(f"UPDATE users SET date='{currentDatetime}' WHERE userBot='{user[1]}'")
                await db.execute(f"UPDATE users SET amountMessages=1 WHERE userBot='{user[1]}'")
                await db.execute(f"UPDATE users SET amountAnswers=1 WHERE userBot='{user[1]}'")

            await db.commit()
        link = f'https://t.me/{botname}?start={user[1]}'
        await message.answer(sendlink(link), parse_mode=types.ParseMode.HTML)
        await state.finish()
        await db.close()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')

@dp.callback_query_handler(text_startswith='a:', state=None)
async def sendanswer(call: types.CallbackQuery, state: FSMContext):
    try:
        dat = call.data.split(':')
        db = await aiosqlite.connect('data.db')
        user = await db.execute(f"SELECT * FROM users WHERE number='{dat[1]}'")
        user = await user.fetchone()

        await sendAnonimAnswer.answer.set()
        async with state.proxy() as data:
            data['to'] = user[0]
            if call.message.text:
                if call.message.text.startswith('Персональная админ панель '):
                    data['answer'] = '«' +  ' '.join(call.message.text.split("\n")[6:])[0:30] + '»'
                elif call.message.text.startswith('Ответ на') or call.message.text.startswith('Опа)'):
                    data['answer'] = '«' +  ' '.join(call.message.text.split('\n')[1:])[0:30] + '»'

            elif call.message.sticker:
                data['answer'] = 'стикер'

            elif call.message.photo:
                data['answer'] = 'фото'

            elif call.message.video:
                data['answer'] = 'видео'

        await bot.send_message(call.message.chat.id, 'Ну что, пиши ответ, раз нажал:', reply_markup=stopkb())
        await db.close()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {call.from_user.id}    {call.from_user.first_name}')


@dp.callback_query_handler(text='otmenans', state=sendAnonimAnswer.answer)
async def stopanswerCMD(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.finish()
        await call.message.edit_text("Ну вот, отправка ответа приостановлена(")
        await asyncio.sleep(3)
        await call.message.delete()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {call.from_user.id}    {call.from_user.first_name}')


@dp.message_handler(content_types=['any'], state=sendAnonimAnswer.answer)
async def sendAnswer(message: types.Message, state: FSMContext):
    if message.text in commandsList:
        await message.delete()
        return
    try:
        db = await aiosqlite.connect('data.db')
        user = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
        user = await user.fetchone()
        userName = f'<a href="tg://user?id={message.from_user.id}">{html.escape(str(message.from_user.first_name))}</a>'

        async with state.proxy() as data:
            answeer = f"<b>Ответ на {html.escape(data['answer'])}...</b>\n\n"

            odmen = await db.execute(f"SELECT * FROM users WHERE userId='{data['to']}'")
            odmen = await odmen.fetchone()

            personal_admin = await bot.get_chat(odmen[0])
            to_admin = f'Персональная админ панель {html.escape(personal_admin.first_name)}\nИмя: {userName} \nФамилия: {html.escape(str(message.from_user.last_name))}\nАйди: {message.from_user.id}\nИмя пользователя: @{str(message.from_user.username)}\n'

            to_user = await db.execute(f'SELECT * FROM users WHERE userId="{data["to"]}"')
            to_user = await to_user.fetchone()
            if to_user is None:
                await message.answer('К сожалению, ты не сможешь ответить на это сообщение, так как адресат уже изменил имя пользователя в ссылке')
                await state.finish()
                return
        

            zxc = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
            zxc = await zxc.fetchone()

            if message.photo:
                if to_user[0] in admins:
                    if message.caption is None:
                        message.caption = ''
                    await bot.send_photo(to_user[0], photo=message.photo[-1].file_id,
                                     caption=to_admin + answeer + html.escape(message.caption),
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=answerkb(zxc[5]))
                else:
                    if message.caption is None:
                        message.caption = ''
                    await bot.send_photo(to_user[0], photo=message.photo[-1].file_id,
                                     caption=answeer + html.escape(message.caption),
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=answerkb(zxc[5]))
            if message.text:
                if to_user[0] in admins:
                    await bot.send_message(to_user[0], text=to_admin + answeer + html.escape(message.text),
                                       parse_mode=types.ParseMode.HTML,
                                       reply_markup=answerkb(zxc[5]))
                else:
                    await bot.send_message(to_user[0], text=answeer + html.escape(message.text),
                                       parse_mode=types.ParseMode.HTML,
                                       reply_markup=answerkb(zxc[5]))
            if message.video:
                if to_user[0] in admins:
                    if message.caption is None:
                        message.caption = ''
                    await bot.send_video(to_user[0], video=message.video.file_id,
                                     caption=to_admin + answeer + html.escape(message.caption),
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=answerkb(zxc[5]))
                else:
                    if message.caption is None:
                        message.caption = ''
                    await bot.send_video(to_user[0], video=message.video.file_id,
                                     caption=answeer + html.escape(message.caption),
                                     parse_mode=types.ParseMode.HTML,
                                     reply_markup=answerkb(zxc[5]))
            if message.sticker:
                if to_user[0] in admins:
                    await bot.send_message(to_user[0], text=to_admin + answeer,
                                       parse_mode=types.ParseMode.HTML)
                else:
                    await bot.send_message(to_user[0], answeer)
                await bot.send_sticker(to_user[0], sticker=message.sticker.file_id,
                                   reply_markup=answerkb(zxc[5]))
            await message.answer('У тебя всё получилось, ответ успешно отправлен😎')
            await state.finish()
            user = await db.execute(f"SELECT * FROM users WHERE userId={message.from_user.id}")
            user = await user.fetchone()

            await db.execute(f"UPDATE users SET answers = {user[6] + 1} WHERE userId='{message.from_user.id}'")
            currentDatetime = datetime.datetime.now().strftime("%d.%m,%Y")
            user = await db.execute(f"SELECT * FROM users WHERE userBot='{user[1]}'")
            user = await user.fetchone()
            if currentDatetime == user[8]:
                await db.execute(f"UPDATE users SET amountAnswers={user[7] + 1} WHERE userBot='{user[1]}'")
            else:
                await db.execute(f"UPDATE users SET date='{currentDatetime}' WHERE userBot='{user[1]}'")
                await db.execute(f"UPDATE users SET amountAnswers=1 WHERE userBot='{user[1]}'")
                await db.execute(f"UPDATE users SET amountMessages=1 WHERE userBot='{user[1]}'")
        await db.commit()
        await db.close()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')

@dp.callback_query_handler(text_startswith='again:', state=None)
async def againCMD(call: types.CallbackQuery, state: FSMContext):
    try:
        userdata = call.data.split(":")[1]
        db = await aiosqlite.connect('data.db')
        cursor = await db.execute(f'SELECT * FROM users WHERE number={int(userdata)}')
        userdata = await cursor.fetchone()
        await sendAnonimMessage.message.set()
        async with state.proxy() as data:
            data['to'] = userdata[1]
        await bot.send_message(call.message.chat.id, 'Хочешь загрузить ещё сообщение? Смело тыкай):')
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {call.from_user.id}    {call.from_user.first_name}')


@dp.message_handler(commands=['setgreet'], state=None)
async def setgreet(message: types.Message):
    try:
        await message.answer(
        'Ну что, пиши новое текстовое приветствие, которое будет видно при переходе по твоей ссылке, твоим фанатам. Только не больше 100 символов, договорились?👉🏻👈🏻 Для отмены напиши .stop')
        await setgreetFSM.greeting.set()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')

@dp.message_handler(content_types=['text'], state=setgreetFSM.greeting)
async def loadGreet(message: types.Message, state: FSMContext):
    if message.text in commandsList:
        await message.delete()
        return
    try:
        db = await aiosqlite.connect('data.db')
        if message.text == '.stop':
            await state.finish()
            await message.answer("Процесс остановлен")
            return
        if len(message.text) > 100:
            await state.finish()
            await message.answer(' А-а-а-й.. с-слишком длинное... приветственное сообщение, мне нужно короче..🥺')
            return
        await db.execute(f"UPDATE users SET mygreet = '{message.text}' WHERE userId = '{message.from_user.id}'")
        await message.answer(
        'Супер, если ты видишь это сообщение, то у тебя всё получилось, приветственное сообщение установлено. Если хочешь его удалить, для этого просто пропиши в новом приветствии слово default в нижнем регистре')
        await state.finish()
        await db.commit()
        await db.close()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')

@dp.message_handler(commands=['stat'])
async def statCMD(message: types.Message):
    try:
        db = await aiosqlite.connect("data.db")
        user = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
        user = await user.fetchone()

        currentDatetime = datetime.datetime.now().strftime("%d.%m,%Y")
        if currentDatetime != user[8]:
            await db.execute(f"UPDATE users SET amountAnswers=0 WHERE userBot='{user[1]}'")
            await db.execute(f"UPDATE users SET amountMessages=0 WHERE userBot='{user[1]}'")

        user = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
        user = await user.fetchone()
        await message.answer(
        f"""Статистика:\n\n\nСообщений сегодня: {user[6]}\nОтветов сегодня: {user[7]}\n\nВсего сообщений: {user[2]}\nВсего ответов: {user[3]}""")
        await db.commit()
        await db.close()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')

@dp.message_handler(commands='setname')
async def setnameCMD(message: types.Message):
    try:
        await message.answer("Имя может содержать только английские символы (заглавные и строчные), "
                             "цифры и нижние подчеркивания, также должно быть не длиннее двадцати символов. \nВведите имя или нажмите на кнопку отмены:")
        await setnameFSM.newname.set()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')

@dp.message_handler(content_types='text', state=setnameFSM.newname)
async def nameCMD(message: types.Message, state: FSMContext):
    if message.text in commandsList:
        await message.delete()
        return
    try:
        async with state.proxy() as data:
            data['name'] = message.text
            data['id'] = message.from_user.id
            if len(data['name']) > 20:
                await state.finish()
                await message.answer("А-а-а-й.. с-слишком длинное... ИМЯ-Я-Я, мне нужно короче..🥺")
                return
        for i in message.text:
            if not i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890_':
                await message.answer("Имя не соответствует правилам. Попробуйте еще раз.")
                await state.finish()
                return
        db = await aiosqlite.connect('data.db')
        user = await db.execute(f"SELECT * FROM users WHERE userBot='{data['name']}'")
        user = await user.fetchone()
        if not user is None:
            await message.answer("Ну блин, это имя уже занято, придумай новое(")
            await state.finish()
            return
        link = f'https://t.me/{botname}?start={data["name"]}'
        await message.answer(f'Установить имя {data["name"]} для ссылки в боте? Ссылка будет выглядеть вот так:\n\n{link}', reply_markup=yesornokb())
        await setnameFSM.next()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')

@dp.callback_query_handler(text='yes', state=setnameFSM.agree)
async def yesCMD(call: types.CallbackQuery, state: FSMContext):
    try:
        db = await aiosqlite.connect('data.db')
        async with state.proxy() as data:
            await db.execute(f"UPDATE users SET userBot='{data['name']}' WHERE userId='{data['id']}'")

        link = f'https://t.me/{botname}?start={data["name"]}'
        await call.message.answer(f"Ура, имя установлено. Вот твоя новая ссылочка):\n\n{link}")
        await state.finish()
        await db.commit()
        await db.close()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {call.from_user.id}    {call.from_user.first_name}')

@dp.callback_query_handler(text='no', state=setnameFSM.agree)
async def noCMD(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.finish()
        await call.message.answer("Создание имени остановлено, может попробуем ещё?..")
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {call.from_user.id}    {call.from_user.first_name}')


@dp.message_handler(commands=['hide'])
async def hideCMD(message: types.Message):
    try:
        if not str(message.from_user.id) in admins:
            return
        if not message.reply_to_message:
            await message.answer('Дурак, я ебу, что прятать? Ответь на сообщение, которое нужно спрятать этой командой ')
            return
        cdata = message.reply_to_message.reply_markup
        if cdata is None:
            await message.answer('Это сообщение не нужно менять')
            return
        cdata = cdata.inline_keyboard
        cdata = dict(*list(*cdata))['callback_data']
        cdata = cdata.split(':')[1:]
        if message.reply_to_message.text:
            msg = message.reply_to_message.text
            await message.reply_to_message.edit_text('\n'.join(msg.split('\n')[5:]), reply_markup=answerkb(cdata[0]))
        elif message.reply_to_message.photo or message.reply_to_message.video:
            msg = message.reply_to_message.caption
            await message.reply_to_message.edit_caption('\n'.join(msg.split('\n')[5:]), reply_markup=answerkb(cdata[0]))
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')

@dp.message_handler(commands=['send'])
async def sendToAll(message: types.Message):
    try:
        if not str(message.from_user.id) in admins:
            return
        if len(message.text) <= 6:
            return
        else:
            await message.answer(message.text[6:], reply_markup=yesorno1Kb())
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')

@dp.callback_query_handler(text_startswith='send:')
async def sendorno(call: types.CallbackQuery):
    try:
        dat = call.data.split(':')[1]
        if dat == 'b':
            return
        db = await aiosqlite.connect('data.db')
        cursor = await db.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        for i in users:
            try:
                await bot.send_message(i[0], text=call.message.text)
            except (aiogram.exceptions.ChatNotFound, aiogram.exceptions.BotBlocked):
                pass
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {call.from_user.id}    {call.from_user.first_name}')

@dp.message_handler()
async def link(message: types.Message):
    try:
        db = await aiosqlite.connect('data.db')
        user = await db.execute(f'SELECT * FROM users WHERE userId={message.from_user.id}')
        user = await user.fetchone()
        link = f'https://t.me/{botname}?start={user[1]}'
        await message.answer(sendlink(link), parse_mode=types.ParseMode.HTML)
        await db.commit()
        await db.close()
        return
    except Exception as error:
        await bot.send_message(int(admins[1]), text=f'Ошибка {error}\nУ пользователя {message.from_user.id}    {message.from_user.first_name}')



if __name__ == '__main__':
    aiogram.executor.start_polling(dispatcher=dp, skip_updates=True)
