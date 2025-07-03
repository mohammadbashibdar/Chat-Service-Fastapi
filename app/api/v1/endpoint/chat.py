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
from app.schemas.enum import SessionType
from app.schemas.base import PaginationInput, Pagination
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


@router.delete("/room/removeMember", response_model=SuccessResponse[RemoveMemberOut],
               responses={404: {"model": ErrorResponse}})
async def delete_room_member(
        data: ChatRoomMemberRemoveInput,
        db: AsyncSession = Depends(get_db),
):
    return await services_chat.remove_member_from_chatroom(data, db)



@router.post("/sendMessage", response_model=SuccessResponse[ChatMessageOut],
             responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}})
async def send_message(
        data: CreateMessageInput,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return await services_chat.send_message(db, data, current_user.id)



@router.get("/chatRoom", response_model=SuccessResponse[ChatRoomResponse],
            responses={400: {"model": ErrorResponse}})
async def get_all_chatRoom(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return await services_chat.get_all_chatRoom(db, current_user)


@router.get("/room/{room_id}/messages", response_model=SuccessResponse[ChatMessagesOut],
            responses={400: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_message_chatroom(
        room_id: int,
        PaginationInput: PaginationInput = Query("pagination things"),
        # count: int = Query(1, description="Page number"),
        # offset: int = Query(10, description="Page size"),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    is_member = await is_user_in_chatroom(db, current_user.id, room_id)
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this chat room.",
        )
    else:
        real_offset = (PaginationInput.count) * (PaginationInput.page)
        pagination_data = Pagination(count=PaginationInput.count, offset=real_offset)
        return await services_chat.get_messages_service(db,pagination_data, room_id)



@router.get("/room/{room_id}/info", response_model=SuccessResponse[ChatRoomInfoOut],
            responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
async def get_room_info(
        room_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    is_member = await is_user_in_chatroom(db, current_user.id, room_id)
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this chat room.",
        )
    else:
        return await services_chat.get_chatRoom_info(db, room_id)


@router.post("/startChatWithUser", response_model=SuccessResponse[ChatRoomInfoOut],
             responses={400: {"model": ErrorResponse}})
async def create_start_message(
        data: PrivateMessageCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return await services_chat.send_private_message_service(db, current_user, data)
