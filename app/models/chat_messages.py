from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP, func, Text, Enum, JSON
from sqlalchemy.orm import relationship
from app.schemas.enum import ChatMessageType, ChatMessageVoteType
from .base import Base


class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(ChatMessageType), nullable=False)  # Assuming this is a string type
    content = Column(Text, nullable=True)
    like = Column(Boolean, default=False, nullable=False)
    dislike = Column(Boolean, default=False, nullable=False)

    chat_room = Column(Integer, ForeignKey('chat_rooms.id', ondelete='CASCADE'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    is_deleted = Column(Boolean, default=False, nullable=False)
    is_edited = Column(Boolean, default=False, nullable=False)

    reply_to = Column(Integer, ForeignKey('chat_messages.id', ondelete='SET NULL'), nullable=True)

    forwarded_from = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    files = Column(Text, nullable=True)  # Assuming files is a JSON or similar type

    private = Column(Boolean, default=False, nullable=False)

    like_count = Column(Integer, default=0, nullable=False)
    dislike_count = Column(Integer, default=0, nullable=False)
    vote_count = Column(Integer, default=0, nullable=False)

    vote_type = Column(Enum(ChatMessageVoteType), nullable=True)  # Assuming this is a string type
    vote_is_anonymous = Column(Boolean, default=False, nullable=False)
    vote_is_optional = Column(Boolean, default=False, nullable=False)
    vote_expiry = Column(TIMESTAMP(timezone=True), nullable=True)
    vote_answers_visible_to = Column(JSON,
                                     nullable=True)  # Assuming this is a JSON or similar type if null vote answers are visible to all
    vote_options = Column(JSON, nullable=True)  # Assuming this is a JSON or similar type
    vote_selected_options = Column(JSON,
                                   nullable=True)  # Assuming this is a JSON or similar type if null vote selected options are visible to all

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now(), nullable=True)

    user_sender = relationship("User", foreign_keys=[sender_id], lazy="joined")