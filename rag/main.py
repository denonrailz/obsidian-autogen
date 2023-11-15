# to test this code
# add your openai key to the config_list on autogen_chat.py
# and to .env file
# run the following code in the same directory
# python main.py
# access http://localhost:8000
# send the following message:
# send ->  What is the status of my order?
# send ->  order 111
# send ->  customer 222
# the response should be Delivered
# send -> exit to end
# CTRL+C terminate the process


from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
import uuid
from autogen_chat import AutogenChat
import asyncio
import uvicorn
from dotenv import load_dotenv, find_dotenv
import openai
import os


_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']
# openai.log='debug'


app = FastAPI()
app.autogen_chat = {}

@app.get("/")
async def get(request: Request):
    chat_id = str(uuid.uuid1())
    html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            function showMessage(msg) {{
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(msg)
                message.appendChild(content)
                messages.appendChild(message)
            }};
            var chat_id = "{chat_id}"
            document.querySelector("#ws-id").textContent = chat_id;
            var ws = new WebSocket("ws://localhost:8000/ws/{chat_id}");
            ws.onmessage = function(event) {{
                showMessage(event.data)
            }};
            function sendMessage(event) {{
                var input = document.getElementById("messageText")
                ws.send(input.value)
                showMessage(input.value)
                input.value = ''
                event.preventDefault()
            }}
        </script>
    </body>
</html>
"""
    return HTMLResponse(html)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[AutogenChat] = []

    async def connect(self, autogen_chat: AutogenChat):
        await autogen_chat.websocket.accept()
        self.active_connections.append(autogen_chat)

    async def disconnect(self, autogen_chat: AutogenChat):
        autogen_chat.client_receive_queue.put_nowait("DO_FINISH")
        print(f"autogen_chat {autogen_chat.chat_id} disconnected")
        self.active_connections.remove(autogen_chat)


manager = ConnectionManager()


async def send_to_client(autogen_chat: AutogenChat):
    while True:
        reply = await autogen_chat.client_receive_queue.get()
        if reply and reply == "DO_FINISH":
            autogen_chat.client_receive_queue.task_done()
            break
        await autogen_chat.websocket.send_text(reply)
        autogen_chat.client_receive_queue.task_done()
        await asyncio.sleep(0.05)


async def receive_from_client(autogen_chat: AutogenChat):
    while True:
        data = await autogen_chat.websocket.receive_text()
        if data and data == "DO_FINISH":
            await autogen_chat.client_receive_queue.put("DO_FINISH")
            await autogen_chat.client_sent_queue.put("DO_FINISH")
            break
        await autogen_chat.client_sent_queue.put(data)
        await asyncio.sleep(0.05)


@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    try:
        autogen_chat = AutogenChat(chat_id=chat_id, websocket=websocket)
        await manager.connect(autogen_chat)
        data = await autogen_chat.websocket.receive_text()
        future_calls = asyncio.gather(send_to_client(autogen_chat), receive_from_client(autogen_chat))
        await autogen_chat.start(data)
        print("DO_FINISHED")
    except Exception as e:
        print("ERROR", str(e))
    finally:
        try:
            await manager.disconnect(autogen_chat)
        except:
            pass

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
