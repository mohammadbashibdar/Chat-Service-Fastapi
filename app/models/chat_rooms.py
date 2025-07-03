from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP, func, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base


class ChatRoom(Base):
    __tablename__ = 'chat_rooms'

    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey('buildings.id', ondelete='SET NULL'), nullable=True)
    name = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)

    read_only = Column(Boolean, default=False, nullable=False)
    mute = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    is_private = Column(Boolean, default=False, nullable=False)
    manager_ids = Column(JSON, nullable=True)  # Assuming this is a JSON or similar type
    profile_image = Column(String(36), nullable=True)  # Assuming this is a JSON or similar type

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now(), nullable=True)

    users = relationship('User', secondary='chat_room_members')
    groups = relationship('Group', secondary='chat_room_members')
    roles = relationship('Role', secondary='chat_room_members')
    buildings = relationship('Building', secondary='chat_room_members')