from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .inventory import Base

class Recipe(Base):
    __tablename__ = 'recipes'

    id = mapped_column(Integer, primary_key=True)
    result_item_id = mapped_column(ForeignKey('items.id'), nullable=False)
    result_item: Mapped["Item"] = relationship("Item", foreign_keys=[result_item_id], overlaps="recipes_as_result")

    ingredients: Mapped["RecipeIngredient"] = relationship("RecipeIngredient", back_populates="recipe")


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    id = mapped_column(Integer, primary_key=True)
    recipe_id = mapped_column(ForeignKey('recipes.id'), nullable=False)
    item_id = mapped_column(ForeignKey('items.id'), nullable=False)
    item: Mapped["Item"] = relationship("Item", foreign_keys=[item_id], overlaps="recipes_as_ingredient")
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)

    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients")