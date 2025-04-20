from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Order, User

# Работа с ордерами-------------------------------------------------------------------
async def orm_add_order(session: AsyncSession, data_order: dict):
    obj = Order(
        order_id=data_order['orderid'],
        description=data_order['description_order'],
    )
    session.add(obj)
    await session.commit()


async def orm_get_orders(session: AsyncSession):
    query = select(Order)
    result = await session.execute(query)
    return result.scalars().all()




async def orm_get_order(session: AsyncSession, uniqid: int):
    query = select(Order).where(Order.order_id == uniqid)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_order(session: AsyncSession, uniqid: int, data_uniq: dict):
    query = update(Order).where(Order.order_id == uniqid).values(
        order_id=data_uniq['uniqid'],
        description=data_uniq['description_uniqid'],
    )
    await session.execute(query)
    await session.commit()


async def orm_delete_order(session: AsyncSession, order_ids: int):
    query = delete(Order).where(Order.order_id == order_ids)
    await session.execute(query)
    await session.commit()

# Работа с пользователями-------------------------------------------------------------------
async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    username: str | None = ' ',
    first_name: str | None = ' ',
    last_name: str | None = ' ',
):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id, username=username, first_name=first_name, last_name=last_name)
        )
        await session.commit()


async def orm_get_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()