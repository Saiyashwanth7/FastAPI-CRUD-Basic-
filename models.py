from database import Base
from sqlalchemy import String, Integer, Column


class Book(Base):
    __tablename__ = "booktable"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(Integer)