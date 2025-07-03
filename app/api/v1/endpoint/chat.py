from fastapi import APIRouter, Depends, Body, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_session
from app.models.user import User
from app.core.dependencies import get_current_user
from app.schemas.chat import ChatRoomCreate, ChatRoomMemberInput, ChatRoomMemberRemoveInput, CreateMessageInput, \
    ChatMessages, ChatMessagesOut, ChatMessages, PrivateMessageCreate, ChatRoomOut, AddMemberOut, DeleteChatroomContact, \
    ChatMessageOut, ChatRoomResponse, ChatRoomInfoOut, \
    MessageOut, RemoveMemberOut
from app.schemas.responses import SuccessResponse, ErrorResponse
from app.schemas.user import SessionBase, UserSimple
from app.crud.chat import is_user_in_chatroom
import app.services.chat as services_chat

router = APIRouter()


@router.post("/room/create", response_model=SuccessResponse[ChatRoomOut],
             responses={404: {"model": ErrorResponse}})
async def create_chat_room(
        data: ChatRoomCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return await services_chat.create_chat_room(db, data, current_user)


@router.put("/room/addMember", response_model=SuccessResponse[AddMemberOut],
            responses={404: {"model": ErrorResponse}})
async def addMember_to_chatroom(
        data: ChatRoomMemberInput,
        db: AsyncSession = Depends(get_db),

):
    return await services_chat.addMember_to_chatroom(db, data)
