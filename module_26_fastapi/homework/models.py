from sqlalchemy import Column, String, Integer, DateTime, Time
from database import Base


class Recipe(Base):
    __tablename__ = 'Recipe'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cooking_time = Column(Integer)
    ingredient_list = Column(String, default='')
    description = Column(String, default='')
    view_count = Column("view_count", Integer, default=0)