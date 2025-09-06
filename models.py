from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    title_ci: Mapped[str] = mapped_column(String, nullable=False, index= True)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
