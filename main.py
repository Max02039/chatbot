from telebot.async_telebot import AsyncTeleBot
import asyncio
import random
from db_made import create_session, get_all, del_session



bot = AsyncTeleBot("6116808706:AAEiglN_jt4Ac9tNS0KdVSm38VYkyesSN40")
active_users = []



@bot.message_handler(commands=["start"])
async def start(message):
    flag = True
    all = get_all()
    for i in all:
        if message.chat.id in i:
            flag = False
    if flag:
        if message.chat.id not in active_users:
            await bot.send_message(message.chat.id, f"Ищем собеседника 🔎, активных пользователей без собеседника: {len(active_users)}")
            active_users.append(message.chat.id)
            await start_chat()
        else:
            await bot.send_message(message.chat.id, f"Вы уже ищете собеседника ✅")
    else:
        await bot.send_message(message.chat.id, f"У вас уже есть активная сессия ❗❗❗")



@bot.message_handler(commands=['stop'])
async def stop(message):
    id2 = del_session(message.chat.id)
    await bot.send_message(message.chat.id, 'Вы закончили общение 😶')
    await bot.send_message(id2, 'Собеседник закончил общение 😱')
async def start_chat():
    if len(active_users) > 1:
        id1 = active_users[0]
        del active_users[0]
        id2 = random.choice(active_users)
        active_users.remove(id2)
        create_session(id1, id2)
        await bot.send_message(id1, f"Собеседник найден 🎉")
        await bot.send_message(id2, f"Собеседник найден 🎉")



def get_second_user(message):
    id2 = None
    all = get_all()
    for i in all:
        if message.chat.id in i:
            if message.chat.id != i[0]:
                id2 = i[0]
            else:
                id2 = i[1]
    return id2



@bot.message_handler(content_types=['text'])
async def send_text(message):
    id2 = get_second_user(message)
    if id2:
        await bot.send_message(id2, message.text)
    else:
        await bot.send_message(message.chat.id, 'У вас нет собеседника 😰')



@bot.message_handler(content_types=['document'])
async def docs(message):
    print(message.document)
    id2 = get_second_user(message)
    file = await bot.get_file(message.document.file_id)
    downloaded = await bot.download_file(file.file_path)
    if id2:
        await bot.send_document(id2, downloaded)
    else:
        await bot.send_message(message.chat.id, 'У вас нет собеседника 😰')



@bot.message_handler(content_types=['voice'])
async def voice(message):
    id2 = get_second_user(message)
    file = await bot.get_file(message.voice.file_id)
    downloaded = await bot.download_file(file.file_path)
    if id2:
        await bot.send_voice(id2, downloaded)
    else:
        await bot.send_message(message.chat.id, 'У вас нет собеседника 😰')



@bot.message_handler(content_types=['photo'])
async def photo(message):
    id2 = get_second_user(message)
    message.photo[-1].width = 2000
    message.photo[-1].height = 2000
    file = await bot.get_file(message.photo[-1].file_id)
    downloaded = await bot.download_file(file.file_path)
    if id2:
        await bot.send_photo(id2, downloaded)
    else:
        await bot.send_message(message.chat.id, 'У вас нет собеседника 😰')

@bot.message_handler(content_types=['video_note'])
async def video_note(message):
    id2 = get_second_user(message)
    file = await bot.get_file(message.video_note.file_id)
    download = await bot.download_file(file.file_path)
    if id2:
        await bot.send_video_note(id2, download)
    else:
        await bot.send_message(message.chat.id, 'У вас нет собеседника 😰')

@bot.message_handler(content_types=['sticker'])
async def sticker(message):
    id2 = get_second_user(message)
    file = await bot.get_file(message.sticker.file_id)
    download = await bot.download_file(file.file_path)
    if id2:
        await bot.send_sticker(id2, download)
    else:
        await bot.send_message(message.chat.id, 'У вас нет собеседника 😰')

@bot.message_handler(content_types=['video'])
async def video(message):
    id2 = get_second_user(message)
    file = await bot.get_file(message.video.file_id)
    download = await bot.download_file(file.file_path)
    if id2:
        await bot.send_video(id2, download)
    else:
        await bot.send_message(message.chat.id, 'У вас нет собеседника 😰')

@bot.message_handler(content_types=['audio'])
async def handle_audio_message(message):
    id2 = get_second_user(message)
    audio_file = await bot.get_file(message.audio.file_id)
    downloaded_file = await bot.download_file(audio_file.file_path)
    if id2:
        await bot.send_audio(id2, downloaded_file)
    else:
        await bot.send_message(message.chat.id, 'У вас нет собеседника 😰')

asyncio.run(bot.polling()) # скучненько