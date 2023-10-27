from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///python.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'books'
    email = Column("email", String, primary_key=True)
    is_subscribed = Column('is_subscribed', Boolean, nullable=False)

    @classmethod
    def get_subscribed_users(cls):
        return session.query(User).where(User.is_subscribed == True).all()

    @classmethod
    def set_user_unsubscribed(cls, email: str):
        user = session.query(User).where(User.email == email).first()
        if user is None:
            item = User(email=email, is_subscribed=False)
            session.add(item)
            session.commit()
        else:
            user.is_subscribed = False
            session.commit()
        return user

    @classmethod
    def set_user_subscribed(cls, email):
        user = session.query(User).where(User.email == email).first()
        if user is None:
            item = User(email=email, is_subscribed=True)
            session.add(item)
            session.commit()
        else:
            user.is_subscribed = True
            session.commit()
        return user


Base.metadata.create_all(bind=engine)
