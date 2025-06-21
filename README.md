Вот обновлённый README с добавленным разделом **Стек технологий**:

---

# CrazyPoizon Telegram Bot

Бот для помощи в расчёте цен и заказа товаров с китайского маркетплейса **POIZON**.  
Позволяет пользователям рассчитать стоимость товара (включая доставку), отследить заказы и связаться с менеджером.

---

## 🧰 Стек технологий

| Категория       | Используемые технологии |
|----------------|-------------------------|
| **Язык**        | Python 3.10+            |
| **Фреймворк**   | Aiogram 3.x             |
| **БД**          | SQLite / PostgreSQL (опционально) |
| **ORM**         | SQLAlchemy (асинхронный) |
| **Миграции БД** | Alembic (опционально)   |
| **Состояния**   | FSM (Finite State Machine) |
| **HTTP-запросы**| AIOHTTP / Requests (при необходимости) |
| **Логирование** | logging                 |
| **Конфигурация**| `.env` файлы / `config.py` |
| **Шаблоны**     | HTML + эмодзи           |

---

## 📋 Описание

Этот Telegram-бот разработан на Python с использованием фреймворка **Aiogram 3.x**, с поддержкой асинхронной работы через **SQLAlchemy ORM** и **SQLite** в качестве базы данных. Бот предоставляет следующие функции:
- Расчёт стоимости товара по категориям.
- Отслеживание состояния заказов.
- Админ-панель для добавления, обновления и удаления заказов.
- Управление списком пользователей.
- Поддержка инлайн-клавиатур и FSM-машины состояний.

---

## 🧠 Бэкенд-архитектура

### 1. **Фреймворк: Aiogram 3.x**
- Используется новейшая версия Aiogram, поддерживающая асинхронные хэндлеры, middleware и FSM.
- Хэндлеры разделены по модулям (`handlers.py`).
- Поддержка команд и callback-запросов через `CallbackQueryHandler`.

### 2. **Состояния: FSM (Finite State Machine)**
- Реализовано несколько состояний:
  - `OrderAdd`: Добавление нового заказа.
  - `OrderUpdate`: Обновление существующего заказа.
  - `OrderDelete`: Удаление заказа.
  - `OrderCheck`: Проверка статуса заказа.
  - `ItemsCheck`: Выбор категории товара и расчёт цены.

### 3. **База данных: SQLite + SQLAlchemy ORM**
- Асинхронное взаимодействие с БД через `asyncio`, `create_async_engine` и `async_sessionmaker`.
- Модели:
  - `User`: Информация о пользователях (ID, имя, username и т.п.).
  - `Order`: Состояние и ID заказа.
- CRUD-операции реализованы через ORM-функции:
  - `orm_add_order`, `orm_get_orders`, `orm_update_order`, `orm_delete_order`
  - `orm_add_user`, `orm_get_users`

#### Пример запроса:
```python
async def orm_get_order(session: AsyncSession, uniqid: int):
    query = select(Order).where(Order.order_id == uniqid)
    result = await session.execute(query)
    return result.scalar()
```

### 4. **Middleware**
- Реализована собственная middleware `DataBaseSession`, которая передает экземпляр `AsyncSession` в каждый handler:
```python
class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)
```

### 5. **Админ-панель**
- Через секретные команды можно управлять заказами:
  - `/add-Smkd` — добавить заказ
  - `/update-SmLg` — обновить заказ
  - `/delete-Smkd` — удалить заказ
  - `/list-orders-Smkv` — список всех заказов
  - `/list-users-Smkd` — список пользователей

---

## 🛒 Калькулятор цен

### Логика расчёта:
- Для каждой категории задан фиксированный markup (наценка).
- Цена товара в юанях умножается на курс юаня (`rate1 = 14.69`) и складывается с наценкой.

Пример:
```python
await message.answer(text=emoji.emojize(f'\U0001F48E<strong> К оплате будет: {round(float(data_calc["quantity"])*rate1+markup)} рублей'))
```

### Поддерживаемые категории:
- Кроссовки, ботинки, куртки, худи, аксессуары и др.
- Наценки различаются по типам товаров.

---

## 🧩 Структура проекта

```
crazy-poizon-bot/
├── app/
│   ├── database/
│   │   ├── models.py      # Модели SQLAlchemy
│   │   ├── orm_query.py   # ORM-запросы
│   │   └── requests.py    # Вспомогательные функции
│   ├── handlers.py        # Основные хэндлеры бота
│   └── keyboard.py        # Inline-клавиатуры
├── middlewares/
│   └── db.py              # Middleware для подключения БД
├── main.py                # Точка входа
├── requirements.txt       # Зависимости
└── config.py              # Конфигурация (токен, URL БД)
```

---

## ⚙️ Установка и запуск

### 1. Установите зависимости:
```bash
pip install -r requirements.txt
```

### 2. Создайте `.env` или измените `config.py`:
```python
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
SQLALCHEMY_URL = 'sqlite+aiosqlite:///./db.sqlite3'
```

### 3. Запустите бота:
```bash
python main.py
```



## 📌 Лицензия

MIT License — см. [LICENSE](LICENSE)

---
