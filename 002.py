import time
from threading import Thread

import websocket

url = 'wss://mrpio-mrpowermanager.onrender.com/ws/'
local_url = 'ws://localhost:8000/ws/'


def on_message(ws, message:bytes):
    print(message)


def on_error(ws, error):
    print(error)
    pass


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def send_all():
        while True:
            ws.send(b"Hello world2222!",websocket.ABNF.OPCODE_BINARY)
            time.sleep(2)
    # Thread(target=send_all).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(local_url + 'mrpio',
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
