from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(Enum('user', 'admin'), default='user')
    ibs_sig = Column(String(100))
    created_at = Column(DateTime, default=func.current_timestamp())
    
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    credit_transactions = relationship("CreditTransaction", back_populates="user", cascade="all, delete-orphan")


class Genre(Base):
    __tablename__ = 'genres'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    
    project_genres = relationship("ProjectGenre", back_populates="genre", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    user = relationship("User", back_populates="projects")
    project_genres = relationship("ProjectGenre", back_populates="project", cascade="all, delete-orphan")
    files = relationship("File", back_populates="project", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="project", cascade="all, delete-orphan")
    registrations = relationship("Registration", back_populates="project", cascade="all, delete-orphan")


class ProjectGenre(Base):
    __tablename__ = 'project_genres'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id', ondelete='CASCADE'), nullable=False)
    
    project = relationship("Project", back_populates="project_genres")
    genre = relationship("Genre", back_populates="project_genres")


class File(Base):
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    path = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=func.current_timestamp())
    
    project = relationship("Project", back_populates="files")


class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    purpose = Column(String(255), nullable=False)
    tempo = Column(String(50), nullable=False)
    key_signature = Column(String(50), nullable=False)
    mood = Column(String(50), nullable=False)
    status = Column(Enum('in_progress', 'completed', 'archived'), default='in_progress')
    created_at = Column(DateTime, default=func.current_timestamp())
    
    project = relationship("Project", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False)
    is_from_ai = Column(Boolean, nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=func.current_timestamp())
    
    conversation = relationship("Conversation", back_populates="messages")


class Registration(Base):
    __tablename__ = 'registrations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    ibs_id = Column(String(255), nullable=False)
    registered_at = Column(DateTime, default=func.current_timestamp())
    
    project = relationship("Project", back_populates="registrations")


class CreditTransaction(Base):
    __tablename__ = 'credit_transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type = Column(Enum('credit', 'debit'), nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_date = Column(DateTime, default=func.current_timestamp())
    
    user = relationship("User", back_populates="credit_transactions")