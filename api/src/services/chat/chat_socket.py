# routes/websocket_routes.py
from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.utils.rag import conversational_rag_chain, rag_answer

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/chating/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        question = await websocket.receive_text()
        answer = rag_answer(question)  # Call the RAG answer function
        await websocket.send_text(answer)


@router.websocket("/chating_aware_history/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        question = await websocket.receive_text()
        answer = conversational_rag_chain.invoke(
            {"input": question},
            config={
                "configurable": {"user_id": "888", "conversation_id": "22"}
            },
        )["answer"]
        await websocket.send_text(answer)
