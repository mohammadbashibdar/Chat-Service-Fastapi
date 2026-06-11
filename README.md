# 🧠 Real-Time Chat Backend with FastAPI

This is a **backend-only real-time chat API** built using **Python**, **FastAPI**.  
All endpoints are available and testable via **Swagger UI**.

---

## 🔧 Features

- ⚡ Real-time communication via Api
- 🧱 Fully backend-based (no frontend required)
- 📄 Interactive API docs using Swagger (OpenAPI)
- 👥 Multi-user chat logic ready to integrate with any frontend
- 🔐 User-based room creation, private chat & messaging

---

## 📦 Tech Stack

- Python 3.10+
- FastAPI
- WebSockets (`fastapi.websockets`)
- Uvicorn (ASGI Server)

---

## 🚀 Getting Started

### 🔧 Install dependencies

It is recommended to use a virtual environment:

```bash
git clone https://github.com/mohammadbashibdar/Chat-Service-Fastapi.git
cd Chat-Fastapi-
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

▶️ Run the server

fastapi dev --host 0.0.0.0 app/main.py

Then open http://localhost:8000/docs in your browser.

🔌 WebSocket Endpoint

ws://localhost:8000/ws/chat/{room_id}

Example message:

{
  "sender_id": 1,
  "room_id": "general",
  "message": "Hello, world!"
}

📁 Project Structure

.
├── main.py
├── models/
├── schemas/
├── services/
├── crud/
├── requirements.txt
└── README.md



📚 API Endpoints

Here are the available endpoints for managing chat rooms and messages:

Method	    Endpoint	                       Description
POST	    /chat/room/create  	               Create Chat Room
PUT	    /chat/room/addMember	       Add Member To Chatroom
DELETE	    /chat/room/removeMember	       Remove Member From Chatroom
POST	    /chat/sendMessage	               Send Message
GET	    /chat/chatRoom	               Get All Chatrooms
GET	    /chat/room/{room_id}/message       Get Messages in Chatroom
GET	    /chat/room/{room_id}/info	       Get Room Info
GET	    /chat/message/{message_id}	       Get Single Message
POST	    /chat/startChatWithUser	       Start One-on-One Chat
GET	    /chat/chatRoomWithUser/{user_id}   Get Private Chatroom With User
GET	    /chat/users/{queryString}	       Search Users by Query


💡 Notes

    This is a backend-only implementation. You can connect your own frontend (React, Vue, Flutter, etc.).

    Swagger UI is included for easy interaction with endpoints.

    Authentication & permissions are supported.

    Open for contributions or ideas!

📫 Contact

Made with ❤️ by Mohammad Bashibdar


# Mohammad Bashibdar
# 2025, IRAN
