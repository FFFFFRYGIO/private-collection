from sqlalchemy import Column, String, UniqueConstraint, Integer

from db.db_create.db_create import Base, db

book_attributes = ['ISBN', 'title', 'authors', 'publishedDate', 'pageCount', 'thumbnail', 'language']


class Book(Base):
    __tablename__ = 'book'
    ISBN = Column(String(50), primary_key=True)
    title = Column(String(270), nullable=False)
    authors = Column(String(110), nullable=False)
    publishedDate = Column(String(10), nullable=True)
    pageCount = Column(Integer, nullable=True)
    thumbnail = Column(String(200), nullable=False)
    language = Column(String(10), nullable=False)
    UniqueConstraint(ISBN, title, authors)


Base.metadata.create_all(db)
