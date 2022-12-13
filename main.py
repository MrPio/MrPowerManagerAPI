import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str,list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, token:str):
        await websocket.accept()
        if token in self.active_connections.keys():
            self.active_connections[token].append(websocket)
        else:
            self.active_connections[token]=[websocket]

    def disconnect(self, websocket: WebSocket,token:str):
        self.active_connections[token].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, websocket: WebSocket,message: bytes,token:str):
        for connection in self.active_connections[token]:
            if connection is not websocket:
                await connection.send_bytes(message)


@app.get("/")
async def root():
    return {"message": "MrPowerMangerAPI"}

manager = ConnectionManager()
@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    await manager.connect(websocket,token)
    try:
        while True:
            data = await websocket.receive_bytes()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(websocket,data,token)
    except WebSocketDisconnect:
        manager.disconnect(websocket,token)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001,reload=True)