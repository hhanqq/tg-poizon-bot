from app.database.models import Order, async_session
from sqlalchemy import select


async def get_orders():
    async with async_session() as session:
        result = await session.execute(select(Order))
        orders = result.scalars().all()
        return orders