
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from src.database.core import AsyncSession

from src.products.models import Product
from src.products.schemas import ProductSchema, ProductOut, OrderProductsSchema
from src.products.exceptions import NotEnoughProducts, ProductNotFound


async def get_all_products(
    db_session: AsyncSession
):
    products = await db_session.scalars(
        sa.Select(Product)
    )

    return [ProductSchema.model_validate(product) for product in products]


async def add_products(
    db_session: AsyncSession,
    products_in
):
    products = await db_session.scalars(
        sa.insert(Product).returning(Product),
        products_in
    )

    await db_session.commit()

    return [ProductSchema.model_validate(product) for product in products]


async def reserve_products(
    db_session: AsyncSession,
    order_products_in: List[OrderProductsSchema],
):
    try:
        for p in order_products_in:
            product = await db_session.scalar(
                sa.Select(Product).where(Product.id == p.id)
            )
            if not product:
                raise ProductNotFound
            
            product.quantity = product.quantity - p.quantity
            # await db_session.execute(
            #     sa.update(Product)
            #         .where(Product.id == product.id)
            #         .values(quantity=Product.quantity-product.quantity)
            # )
        await db_session.commit()
    except IntegrityError as e:
        raise NotEnoughProducts from e
    


async def backward_reserved_products(
    db_session: AsyncSession,
    order_products_in: List[OrderProductsSchema],
):
    for product in order_products_in:
        await db_session.execute(
            sa.update(Product)
                .where(Product.id == product.id)
                .values(quantity=Product.quantity+product.quantity)
        )
    await db_session.commit()
    