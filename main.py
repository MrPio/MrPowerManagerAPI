import uvicorn
from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "MrPowerMangerAPI"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        await websocket.send_text(f"Message text was: {data}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)