from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, mapped_column, Mapped

engine = create_engine("sqlite:///python.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column("name", String, nullable=False)
    count = Column('count', Integer, default=1)
    release_date = Column('release_date', DateTime(timezone=True), nullable=True)
    author_id = Column(ForeignKey('authors.id'), nullable=False, doc='автор', comment='автор')
    author = relationship("Author", back_populates='authors')

    def __repr__(self):
        return self.id

    @classmethod
    def get_all_books(cls):
        return session.query(Book).all()


class Author(Base):
    __tablename__ = 'authors'

    id = Column("id", Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    surname = Column('surname', String, nullable=False)


class Student(Base):
    __tablename__ = 'students'

    id = Column("id", Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    surname = Column('surname', String, nullable=False)
    phone = Column('phone', String, nullable=False)
    email = Column('email', String, nullable=False)
    average_score = Column('average_score', Float, nullable=False)
    scholarship = Column('scholarship', Boolean, nullable=False)

    @classmethod
    def get_all_students_with_scholarship(cls):
        return session.query(Student).where(Student.scholarship is True).all()

    @classmethod
    def get_all_student_by_average_score(cls, average_score: float):
        return session.query(Student).where(Student.average_score > average_score).all()

    @classmethod
    def get_by_id(cls, id):
        return session.query(Student).where(Student.id == id).first()


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    id = Column("id", Integer, primary_key=True)
    book_id = Column(ForeignKey('books.id'), nullable=False, doc='книга', comment='книга')
    book = relationship("Book", back_populates='books')
    student_id = Column(ForeignKey('students.id'), nullable=False, doc='студент', comment='студент')
    student = relationship("Student", back_populates='students')
    date_of_issue = Column('date_of_issue', DateTime, nullable=False)
    date_of_return = Column('date_of_return', DateTime)

    @hybrid_property
    def count_date_with_book(self) -> int:
        if self.date_of_return is not None:
            return (self.date_of_return - self.date_of_issue).days
        else:
            return (datetime.today().date() - self.date_of_issue).days

    @classmethod
    def get_debtors(cls):
        return session.query(ReceivingBook).all()

    @classmethod
    def give_to_student(cls, id_book, id_student):
        item = ReceivingBook(student_id=int(id_student), book_id=int(id_book), date_of_issue=datetime.today())
        session.add(item)
        session.commit()
        return item

    @classmethod
    def hand_over_the_book(cls, id_book, id_student):
        items = session.query(ReceivingBook).where(
            ReceivingBook.student_id == int(id_student) and ReceivingBook.book_id == int(id_book)).all()
        for item in items:
            item.date_of_return = datetime.utcnow()
        session.commit()
        return items


Base.metadata.create_all(bind=engine)
