import uvicorn
from fastapi import FastAPI, WebSocket

app = FastAPI(
    title='OpenApi Proxy'
)
app.autogen_chat = {}


@app.get("/hello/")
def hello():
    print('Hello world!')
    return 'Hello world!'


@app.websocket("/")
async def send_data(websocket: WebSocket):
    print('CONNECTING...')
    await websocket.accept()
    while True:
        try:
            await websocket.receive_text()
            resp = {
                "message": "message from websocket"
            }
            await websocket.send_json(resp)
        except Exception as e:
            print(e)
            break
    print("CONNECTION DEAD...")

if __name__ == "__main__":
    uvicorn.run("proxy:app", host="127.0.0.1", port=8000, reload=True)
