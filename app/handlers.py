from aiogram import types, Router
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime
from app.models import User, MessageTemplate, ScheduledMessage

router = Router()


class CreateMessage(StatesGroup):
    content = State()
    image = State()
    video = State()
    save_template = State()


class ScheduleMessage(StatesGroup):
    template_id = State()
    send_at = State()


@router.message(Command(commands='start'))
async def cmd_start(message: types.Message):
    user, created = User.get_or_create(user_id=message.from_user.id)
    await message.reply("Добро пожаловать! Используйте /create для создания нового сообщения.")


@router.message(Command(commands='create'))
async def cmd_create(message: types.Message, state: FSMContext):
    await state.set_state(CreateMessage.content)
    await message.reply("Пожалуйста, отправьте текстовое содержание сообщения.")


@router.message(StateFilter(CreateMessage.content))
async def process_content(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    await state.set_state(CreateMessage.image)
    await message.reply(
        "Отправьте URL изображения для сообщения. Введите 'skip', если не хотите добавлять изображение.")


@router.message(StateFilter(CreateMessage.image))
async def process_image(message: types.Message, state: FSMContext):
    if message.text.lower() != 'skip':
        await state.update_data(image=message.text)
    await state.set_state(CreateMessage.video)
    await message.reply("Отправьте URL видео для сообщения. Введите 'skip', если не хотите добавлять видео.")


@router.message(StateFilter(CreateMessage.video))
async def process_video(message: types.Message, state: FSMContext):
    if message.text.lower() != 'skip':
        await state.update_data(video=message.text)
    await state.set_state(CreateMessage.save_template)
    await message.reply("Хотите сохранить это как шаблон? Введите 'да' или 'нет'.")


@router.message(StateFilter(CreateMessage.save_template))
async def process_save_template(message: types.Message, state: FSMContext):
    data = await state.get_data()
    content = data.get('content')
    image = data.get('image', None)
    video = data.get('video', None)

    if message.text.lower() == 'да':
        MessageTemplate.create(content=content, image=image, video=video)
        await message.reply("Шаблон сообщения сохранён. Используйте /schedule для его запланирования.")
    elif message.text.lower() == 'нет':
        await message.reply("Шаблон сообщения не сохранён. Используйте /schedule, если хотите запланировать без сохранения.")
    else:
        await message.reply("Не понял ваш ответ. Пожалуйста, введите 'да' или 'нет'.")
        return

    await state.set_state(None)

@router.message(Command(commands='schedule'))
async def cmd_schedule(message: types.Message, state: FSMContext):
    await state.set_state(ScheduleMessage.template_id)
    templates = MessageTemplate.select()
    await message.reply("Пожалуйста, выберите ID шаблона для запланирования:")
    for template in templates:
        await message.reply(f"ID: {template.id}, Содержание: {template.content[:50]}...")


@router.message(StateFilter(ScheduleMessage.template_id))
async def process_template_id(message: types.Message, state: FSMContext):
    template_id = message.text
    await state.update_data(template_id=template_id)
    await state.set_state(ScheduleMessage.send_at)
    await message.reply("Укажите, когда отправить это сообщение. Используйте формат 'DD-MM-YYYY HH:MM'.")


@router.message(StateFilter(ScheduleMessage.send_at))
async def process_send_at(message: types.Message, state: FSMContext):
    send_at_str = message.text

    try:
        send_at = datetime.strptime(send_at_str, '%d-%m-%Y %H:%M')
    except ValueError:
        await message.reply("Неверный формат. Пожалуйста, используйте 'DD-MM-YYYY HH:MM'")
        return

    data = await state.get_data()
    template_id = data.get('template_id')

    template = MessageTemplate.get_by_id(template_id)
    user = User.get(user_id=message.from_user.id)

    ScheduledMessage.create(template=template, user=user, send_at=send_at)

    await message.reply("Сообщение запланировано.")
    await state.set_state(None)
