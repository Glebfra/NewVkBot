import openai
from vkbottle import BaseStateGroup, CtxStorage
from vkbottle.bot import Blueprint, Message

bp = Blueprint("ChatGPT")
ctx_storage = CtxStorage()

openai.api_key = ctx_storage.get('open_ai_token')


class States(BaseStateGroup):
    CHAT_GPT_STATE = 'chat_gpt'


class Routes(object):
    start_messaging = ['ChatGPT']


@bp.on.message(text=Routes.start_messaging)
async def start_messaging(message: Message):
    await bp.state_dispenser.set(message.peer_id, States.CHAT_GPT_STATE)
    return await message.answer(
        'Активирую CHAT_GPT. Начните общение с ним :-)',
        keyboard=ctx_storage.get('back_keyboard').get_keyboard()
    )


@bp.on.message(state=States.CHAT_GPT_STATE)
async def on_chat_gpt_message(message: Message):
    if message.text == 'Назад':
        await bp.state_dispenser.delete(message.peer_id)
        return await message.answer(
            'Возвращаюсь назад',
            keyboard=ctx_storage.get('default_keyboard').get_keyboard()
        )

    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message.text,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return await message.answer(
        completion.choices[0].text,
        keyboard=ctx_storage.get('back_keyboard').get_keyboard()
    )

