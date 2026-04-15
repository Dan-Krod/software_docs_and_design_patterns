from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

member_roles = Table(
    'member_roles', Base.metadata,
    Column('member_id', Integer, ForeignKey('members.id')),
    Column('role_id', Integer, ForeignKey('roles.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    status = Column(String(50))
    type = Column(String(50)) 
    password_hash = Column(String(200))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

class ServerOwner(User):
    __tablename__ = 'server_owners'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    owner_since = Column(DateTime, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'owner',
    }

class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    member_count = Column(Integer, default=0) 
    invite_code = Column(String(20), unique=True)

    channels = relationship("Channel", back_populates="server", cascade="all, delete-orphan")
    roles = relationship("Role", back_populates="server", cascade="all, delete-orphan")
    
    members = relationship("Member", back_populates="server")

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    server_id = Column(Integer, ForeignKey('servers.id'))
    nickname = Column(String(100))
    joined_at = Column(DateTime, default=datetime.utcnow)
    is_muted = Column(Boolean, default=False)

    user = relationship("User")
    server = relationship("Server", back_populates="members")
    roles = relationship("Role", secondary=member_roles)
    messages = relationship("Message", back_populates="author")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    name = Column(String(50))
    
    server = relationship("Server", back_populates="roles")

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey('servers.id'))
    title = Column(String(100))
    is_locked = Column(Boolean, default=False)
    type = Column(String(50))

    server = relationship("Server", back_populates="channels")

    __mapper_args__ = {
        'polymorphic_identity': 'channel',
        'polymorphic_on': type
    }

class TextChannel(Channel):
    __tablename__ = 'text_channels'
    id = Column(Integer, ForeignKey('channels.id'), primary_key=True)
    slow_mode_delay = Column(Integer, default=0)

    messages = relationship("Message", back_populates="channel", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'text_channel',
    }

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('text_channels.id'))
    author_id = Column(Integer, ForeignKey('members.id'))
    content = Column(String(2000))
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(String(500)) 

    channel = relationship("TextChannel", back_populates="messages")
    author = relationship("Member", back_populates="messages")