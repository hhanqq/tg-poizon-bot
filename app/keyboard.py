from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import emoji

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=emoji.emojize('Рассчитать стоимость \U000026E9'), callback_data='price')],
    [InlineKeyboardButton(text=emoji.emojize('Оформить заказ \U0001F680'), callback_data='req-to-buy')],
    [InlineKeyboardButton(text=emoji.emojize('Отследить заказ \U0001F30E'), callback_data='check-order')],
    [InlineKeyboardButton(text=emoji.emojize('Акции \U0001F4A0'), callback_data='promotion'),InlineKeyboardButton(text=emoji.emojize('Отзывы \U0001F4EB'), callback_data='reviews', url='https://t.me/crazypoizon')],
    [InlineKeyboardButton(text=emoji.emojize('Обучение использования POIZON :books:'), callback_data='guide')]], resize_keyboard=True)

items = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=emoji.emojize('Кроссовки \U0001F45F'), callback_data='cat_picked_sneakers')],
    [InlineKeyboardButton(text=emoji.emojize('Ботинки \U0001F45E'), callback_data='cat_picked_boots')],
    [InlineKeyboardButton(text=emoji.emojize('Зимние куртки \U00002744'), callback_data='cat_picked_winter-jacket')],
    [InlineKeyboardButton(text=emoji.emojize('Осенние, весенние куртки :coat:'), callback_data='cat_picked_other-jacket')],
    [InlineKeyboardButton(text=emoji.emojize('Ветровки \U0001F97C'), callback_data='cat_picked_light-jacket')],
    [InlineKeyboardButton(text=emoji.emojize('Худи :kimono:'), callback_data='cat_picked_hoodie')],
    [InlineKeyboardButton(text=emoji.emojize('Аксессуары \U0001F97D'), callback_data='cat_picked_accessories')],
    [InlineKeyboardButton(text=emoji.emojize('Украшения, парфюм, брелки :ring:'), callback_data='cat_picked_jewelry-perfume-keychain')],
    [InlineKeyboardButton(text=emoji.emojize('Футболки, лонгсливы, шорты \U0001F455'), callback_data='cat_picked_tshirt-longsleeve-shorts')],
    [InlineKeyboardButton(text=emoji.emojize('Телефоны \U0001F4F1'), callback_data='cat_picked_telephone')],
    [InlineKeyboardButton(text=emoji.emojize('Ноутбуки \U0001F4BB'), callback_data='cat_picked_laptop')],
    [InlineKeyboardButton(text=emoji.emojize('Платья \U0001F457'), callback_data='cat_picked_dress')],
    [InlineKeyboardButton(text=emoji.emojize('Штаны, джинсы \U0001F456'), callback_data='cat_picked_pants')],
    [InlineKeyboardButton(text=emoji.emojize('Сумки большие \U0001F45C'), callback_data='cat_picked_big-bag')],
    [InlineKeyboardButton(text=emoji.emojize('Сумки маленькие \U0001F45D'), callback_data='cat_picked_small-bag')],
    [InlineKeyboardButton(text=emoji.emojize('Телевизоры, мониторы \U0001F5A5'), callback_data='cat_picked_tv-monitor')],
    [InlineKeyboardButton(text=emoji.emojize('Игровые девайсы \U0001F5B1'), callback_data='cat_picked_gaming-device')]])

back_check_price = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=emoji.emojize('Рассчитать цену нового товара :counterclockwise_arrows_button:'), callback_data='check-new-item')],
    [InlineKeyboardButton(text=emoji.emojize('Оформить заказ :airplane:'), callback_data='req-to-buy')],
    [InlineKeyboardButton(text=emoji.emojize('Главное меню :circled_M:'), callback_data='main-menu')]])

back_main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=emoji.emojize('Главное меню :circled_M:'), callback_data='main-menu')]])

buy_item = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=emoji.emojize('Оформить заказ \U0001F680'), callback_data='req-to-buy')]
])