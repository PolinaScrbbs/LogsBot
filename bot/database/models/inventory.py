from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as BaseEnum

from .users import Base

class ItemRarity(BaseEnum):
    COMMON  = "Обычный"
    UNCOMMON  = "Необычная"
    RARE  = "Редкая"
    EPIC  = "Эпическая"
    LEGENDARY  = "Легендарная" 

class Item(Base):
    __tablename__ = 'items'

    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(24), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    rarity = mapped_column(Enum(ItemRarity), nullable=False)

    recipes_as_result: Mapped["Recipe"] = relationship("Recipe", foreign_keys="[Recipe.result_item_id]", overlaps="result_item")
    recipes_as_ingredient: Mapped["RecipeIngredient"] = relationship("RecipeIngredient", foreign_keys="[RecipeIngredient.item_id]", overlaps="item")

class Inventory(Base):
    __tablename__ = 'inventory'

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="inventory")

inventory_items = Table('inventory_items', Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('inventory_id', Integer, ForeignKey('inventory.id'))
)