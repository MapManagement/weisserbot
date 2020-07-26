import websockets
import json
import asyncio
import uuid
from bot.utils import secrets


class WebSocket():

    def __init__(self):
        self.topics = ["channel-points-channel-v1.87252610"]

    async def connect(self):
        self.connection = await websockets.client.connect("wss://pubsub-edge.twitch.tv")
        if self.connection.open:
            message = {"type": "LISTEN", "nonce": str(self.create_nonce()),
                       "data":
                           {"topics": self.topics, "auth_token": secrets.websocket_token}}

            json_message = json.dumps(message)
            await self.send_message(json_message)
            return self.connection

    async def receive_message(self, connection):
        while True:
            try:
                message = await connection.recv()

                print(f"Received: {message}")
            except websockets.exceptions.ConnectionClosed:
                break

    async def send_message(self, message):
        await self.connection.send(message)

    def create_nonce(self):
        nonce = uuid.uuid1()
        nonce_oauth = nonce.hex
        return nonce_oauth
