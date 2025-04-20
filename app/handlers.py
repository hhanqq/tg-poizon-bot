import emoji

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.orm_query import orm_add_order, orm_update_order, orm_get_order, orm_delete_order, orm_get_orders, \
    orm_add_user, orm_get_users
from app.database.requests import get_orders

import app.keyboard as kb


router = Router()

rate1 = 14.69
markups = {
    'sneakers': 2100,
    'boots': 2600,
    'winter-jacket': 2100,
    'other-jacket': 2100,
    'light-jacket': 1600,
    'hoodie': 1600,
    'accessories': 1300,
    'jewelry-perfume-keychain': 1300,
    'tshirt-longsleeve-shorts': 1400,
    'telephone': 3600,
    'laptop': 4600,
    'dress': 2100,
    'pants': 1350,
    'big-bag': 2100,
    'small-bag': 1350,
    'tv-monitor': 5100,
    'gaming-device': 2100,
}

class ItemsCheck(StatesGroup):
    quantity = State()

class OrderCheck(StatesGroup):
    state_order_id = State()

class OrderAdd(StatesGroup):
    orderid = State()
    description_order = State()
    updated_order = State()

class OrderUpdate(StatesGroup):
    uniqid = State()
    description_uniqid = State()
    order_for_update = None

class OrderDelete(StatesGroup):
    order_ids = State()


file_ids = {}

async def send_message_with_photo(bot, file_name, text, chat_id, reply_markup):
    try:
        if file_name not in file_ids.keys():
            file_ids[file_name] = (await bot.send_photo(
                chat_id=chat_id,
                photo=FSInputFile(file_name),
                reply_markup=reply_markup,
                caption=text,
            )).photo[0].file_id

        else:
            await bot.send_photo(
                chat_id=chat_id,
                photo=file_ids[file_name],
                reply_markup=reply_markup,
                caption=text,
            )
    except Exception as e:
        print(e)



# Добавление ордеров в БД -----------------------------------------------------------------
@router.message(F.text == 'add-SmkdLgvnw23!0S@64fmsqQ')
async def admin_add_order(message: Message, state: FSMContext):
    await state.set_state(OrderAdd.orderid)
    await message.answer('Введите order id')

@router.message(OrderAdd.orderid)
async def orderid(message: Message, state: FSMContext):
    await state.update_data(orderid=message.text)
    await state.set_state(OrderAdd.description_order)
    await message.answer('Введите состояние заказа')

@router.message(OrderAdd.description_order)
async def description_order(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description_order=message.text)
    await message.answer('Успешно')
    data_order = await state.get_data()
    await orm_add_order(session, data_order)
    await state.clear()

# Обновление состояние ордера в БД -------------------------------------------------------------
@router.message(F.text == 'update-SmkdLgvnw23!0S@64fmsqQ')
async def admin_update_order(message: Message, state: FSMContext):
    await state.set_state(OrderUpdate.uniqid)
    await message.answer('Введите order id')

@router.message(OrderUpdate.uniqid)
async def uniqid_for_order(message: Message, state: FSMContext):
    await state.update_data(uniqid=message.text)
    await state.set_state(OrderUpdate.description_uniqid)
    await message.answer('Введите новое состояние заказа')

@router.message(OrderUpdate.description_uniqid)
async def description_uniqid(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description_uniqid=message.text)
    await message.answer('Успешно')
    data_uniq = await state.get_data()
    uniqid = int(data_uniq["uniqid"])
    order_for_update = await orm_get_order(session, uniqid)
    await orm_update_order(session,order_for_update.order_id, data_uniq)

    await state.clear()

# Удаление ордеров из БД -------------------------------------------------------------
@router.message(F.text == 'delete-SmkdLgvnw23!0S@64fmsqQ')
async def admin_del_order(message: Message, state: FSMContext):
    await state.set_state(OrderDelete.order_ids)
    await message.answer('Введите order id')

@router.message(OrderDelete.order_ids)
async def order_del(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(order_ids=message.text)
    await message.answer('Успешно')
    data_del = await state.get_data()
    order_ids = data_del["order_ids"]
    await orm_delete_order(session, order_ids)

    await state.clear()

# Список всех ордеров из БД--------------------------------------------------------------
@router.message(F.text == 'list-orders-SmkdLgvnw23!0S@64fmsqQ')
async def admin_list(message: Message, session: AsyncSession):
    for order in await orm_get_orders(session):
        await message.answer(f'Order id: {order.order_id}\n\nСтатус: {order.description}\n\n')\

# Список всех юзеров из БД----------------------------------------------------------------------
@router.message(F.text == 'list-users-SmkdLgvnw23!0S@64fmsqQ')
async def user_list(message: Message, session: AsyncSession):
    for user in await orm_get_users(session):
        await message.answer(f'id: {user.id} <a href="tg://user?id={user.user_id}">{user.user_id}</a>, @{user.username} {user.first_name} {user.last_name}')

# Основной код----------------------------------------------------------------------
@router.message(CommandStart())
async def get_photo_and_message(message: Message, session: AsyncSession):
    await orm_add_user(session, user_id=message.from_user.id, username=message.from_user.username, first_name=message.from_user.first_name, last_name=message.from_user.last_name)
    await send_message_with_photo(
        chat_id=message.chat.id,
        file_name='media/logo crazy poizon.png',
        text=f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a><a><strong>, Вас приветствует бот для помощи в расчёте цен и заказа вещей с китайского маркетплейса POIZON!</strong></a>',
        reply_markup=kb.main,
        bot=message.bot
    )


@router.callback_query(F.data == 'price')
async def check_price(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    await callback.message.answer(text=emoji.emojize(f'<strong>Выберите нужную категорию товара</strong> \U0001F4CD'), reply_markup=kb.items)
    await callback.message.edit_reply_markup(reply_markup=None)

@router.callback_query(F.data == 'check-new-item')
async def check_new_item(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    await callback.message.answer(text=emoji.emojize(f'<strong>Выберите нужную категорию товара</strong> \U0001F4CD'), reply_markup=kb.items)

@router.callback_query(F.data == 'req-to-buy')
async def req_to_buy(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    await callback.message.answer(text=emoji.emojize(f'<strong>:technologist_light_skin_tone:Для оформления заказа, свяжитесь с нашим менеджером\n@money_alipay</strong>'))

@router.callback_query(F.data == 'promotion')
async def check_promotion(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    await callback.message.answer(text=emoji.emojize(f'<strong>\U00002757Акция действует до 31.12.2024 при покупке от 2-х вещей\U00002757\n\n\U00002744  Скидка на первый заказ - 555₽  \U00002744</strong>'),reply_markup=kb.buy_item)

@router.callback_query(F.data == 'main-menu')
async def main_menu(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    await send_message_with_photo(
        chat_id=callback.message.chat.id,
        file_name='media/logo crazy poizon.png',
        text=f'<a href="tg://user?id={callback.from_user.id}">{callback.from_user.full_name}</a><a><strong>, Вас приветствует бот для помощи в расчёте цен и заказа вещей с китайского маркетплейса POIZON!</strong></a>',
        reply_markup=kb.main,
        bot=callback.bot
    )


@router.callback_query(F.data == 'check-order')
async def check_order(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderCheck.state_order_id)
    await callback.answer('', show_alert=False)
    await callback.message.answer(text=emoji.emojize(f'<strong>:memo: Введите уникальный номер заказа, который был выдан менеджером!</strong>'))

@router.message(OrderCheck.state_order_id)
async def check_order_id(message: Message, state: FSMContext):
    await state.update_data(state_order_id=message.text)
    data_order = await state.get_data() # 123145
    orders = await get_orders()
    for order in orders:
        if int(data_order["state_order_id"]) == int(order.order_id):
            await message.answer(text=emoji.emojize(f'<strong>\U0001F4E6Ваш заказ под номером: {order.order_id}\n\n:bell:Статус: {order.description}</strong>'), reply_markup=kb.back_main_menu)
            await state.clear()

@router.callback_query(F.data == 'guide')
async def guide(callback: CallbackQuery):
    await callback.answer('', show_alert=False)
    await callback.message.answer(text=emoji.emojize(f'<strong>Совсем скоро появится обучающий материал\U00002757</strong>'))

#----------------------------------------------------------------
# Работа с категориями
#----------------------------------------------------------------


@router.callback_query(F.data.startswith('cat_picked'))
async def cat_picked(callback: CallbackQuery, state: FSMContext):
    cat = callback.data.split('_')[-1]
    await state.set_state(ItemsCheck.quantity)
    await state.update_data(cat=cat)
    await send_message_with_photo(
        bot=callback.bot,
        file_name='media/guidepoizon.jpg',
        text=emoji.emojize(
            f'<strong>Введите цену товара в ¥ (Юанях) :China:\n\nСумма к оплате указана с доставкой до г.Томск, последующая доставка до вашего города оформляется через СДЕК за отдельную плату\U00002757\n\nДля жителей г.Томска, последующая доставка курьером от нашего склада до вашего адреса - осуществляется за наш счет \U0001F4B8\n\nПожалуйста, ознакомьтесь с фото-инструкцией выше</strong> :blue_book:'),
        reply_markup=None,
        chat_id=callback.message.chat.id,
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.answer()

@router.message(ItemsCheck.quantity)
async def req_quantity_calc_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(f'<strong>Введите целое число!</strong>')
        return

    cat = (await state.get_data())['cat']
    markup = markups[cat]
    int(message.text)
    await state.update_data(quantity=message.text)
    data_calc = await state.get_data()
    await message.answer(text=emoji.emojize(f'\U0001F48E<strong> К оплате будет: {round(float(data_calc["quantity"])*rate1+markup)} рублей\n\n\U0001F310 Курс юаня: {rate1}</strong>'), reply_markup=kb.back_check_price)
    await state.clear()















