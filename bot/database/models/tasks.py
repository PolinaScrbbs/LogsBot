from sqlalchemy import DateTime, Integer, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as BaseEnum
from datetime import datetime

from .recipes import Base

class TaskType(BaseEnum):
    DAILY = "Ежедневное"
    WEEKLY = "Еженедельное"
    LIMITED = "Лимитированное"

class Task(Base):
    __tablename__ = "tasks"

    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    type = mapped_column(Enum(TaskType), default=TaskType.DAILY, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(True), default=None, nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime(True), default=None, nullable=True)

class TaskReward(Base):
    __tablename__ = 'task_rewards'

    id = mapped_column(Integer, primary_key=True)
    task_id = mapped_column(ForeignKey('tasks.id'), nullable=False)
    item_id = mapped_column(ForeignKey('items.id'), nullable=False)
    item: Mapped["Item"] = relationship(foreign_keys=[item_id])
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)

class Result(Base):
    __tablename__ = 'task_results'

    id = mapped_column(Integer, primary_key=True)
    user_id =  mapped_column(ForeignKey('users.id'), nullable=False)
    task_id = mapped_column(ForeignKey('tasks.id'), nullable=False)
    execution_time: Mapped[datetime] = mapped_column(DateTime(True), server_default=func.now())
    