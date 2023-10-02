from aiogram import Bot, Dispatcher, types, Router
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext
from configs.config import API_TOKEN
from datetime import datetime
from models import User, MessageTemplate, ScheduledMessage

bot = Bot(token=API_TOKEN)
storage = RedisStorage2(host="localhost", port=6379, db=5)
dp = Dispatcher(bot, storage=storage)
router = Router()


# FSM States
class CreateMessage(StatesGroup):
    content = State()
    image = State()
    video = State()
    save_template = State()


@router.message(Command(commands='start'))
async def cmd_start(message: types.Message):
    user, created = User.get_or_create(user_id=message.from_user.id)
    await message.reply("Welcome! Use /create to create a new message.")


# FSM to create a new message
@router.message(Command(commands='create'))
async def cmd_create(message: types.Message, state: FSMContext):
    await state.set_state(CreateMessage.content)
    await message.reply("Please, send the text content for the message.")


@router.message(StateFilter(CreateMessage.content))
async def process_content(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    await state.set_state(CreateMessage.image)
    await message.reply("Send an image URL for the message. Type 'skip' if you don't want to add an image.")


@router.message(StateFilter(CreateMessage.image))
async def process_image(message: types.Message, state: FSMContext):
    if message.text.lower() != 'skip':
        await state.update_data(image=message.text)
    await state.set_state(CreateMessage.video)
    await message.reply("Send a video URL for the message. Type 'skip' if you don't want to add a video.")


@router.message(StateFilter(CreateMessage.video))
async def process_video(message: types.Message, state: FSMContext):
    if message.text.lower() != 'skip':
        await state.update_data(video=message.text)
    await state.set_state(CreateMessage.save_template)
    await message.reply("Do you want to save this as a template? Type 'yes' or 'no'.")


@router.message(StateFilter(CreateMessage.save_template))
async def process_save_template(message: types.Message, state: FSMContext):
    data = await state.get_data()
    content = data.get('content')
    image = data.get('image', None)
    video = data.get('video', None)

    if message.text.lower() == 'yes':
        MessageTemplate.create(content=content, image=image, video=video)

    await message.reply("Message created. Use /schedule to schedule this message.")
    await state.set_state(None)


# FSM States for scheduling messages
class ScheduleMessage(StatesGroup):
    template_id = State()
    send_at = State()


@router.message(Command(commands='schedule'))
async def cmd_schedule(message: types.Message, state: FSMContext):
    await state.set_state(ScheduleMessage.template_id)
    templates = MessageTemplate.select()
    await message.reply("Please choose a template ID to schedule:")
    for template in templates:
        await message.reply(f"ID: {template.id}, Content: {template.content[:50]}...")


@router.message(StateFilter(ScheduleMessage.template_id))
async def process_template_id(message: types.Message, state: FSMContext):
    template_id = message.text
    await state.update_data(template_id=template_id)
    await state.set_state(ScheduleMessage.send_at)
    await message.reply("Please specify when to send this message. Use the format 'YYYY-MM-DD HH:MM:SS'.")


@router.message(StateFilter(ScheduleMessage.send_at))
async def process_send_at(message: types.Message, state: FSMContext):
    send_at_str = message.text
    send_at = datetime.strptime(send_at_str, '%Y-%m-%d %H:%M:%S')

    data = await state.get_data()
    template_id = data.get('template_id')

    template = MessageTemplate.get_by_id(template_id)
    user = User.get(user_id=message.from_user.id)

    ScheduledMessage.create(template=template, user=user, send_at=send_at)

    await message.reply("Message has been scheduled.")
    await state.set_state(None)
