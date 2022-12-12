import asyncio

import websockets


async def hello():
    async with websockets.connect("ws://mrpio.deta.dev/ws") as websocket:
        await websocket.send(b"Hello world!")
        data = await websocket.recv()
        print(data)


asyncio.run(hello())
