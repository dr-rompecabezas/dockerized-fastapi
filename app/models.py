from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    owner = relationship('User')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = 'votes'
    post_id = Column(Integer, ForeignKey(
        'posts.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    post = relationship('Post')
    user = relationship('User')