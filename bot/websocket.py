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
                self.check_reward(message)
            except websockets.exceptions.ConnectionClosed:
                break

    async def send_message(self, message):
        await self.connection.send(message)

    def create_nonce(self):
        nonce = uuid.uuid1()
        nonce_oauth = nonce.hex
        return nonce_oauth

    def check_reward(self, reward):
        json_reward = json.loads(reward)
        print(json_reward)

        if json_reward['type'] == "MESSAGE":
            message_data = json_reward['data']['message']
            json_message = json.loads(message_data)
            reward_name = json_message['data']['redemption']['reward']['title']
            print(reward_name)


if __name__ == "__main__":
    websocket = WebSocket()
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(websocket.connect())

    task = [asyncio.ensure_future(websocket.receive_message(connection=connection))]
    loop.run_until_complete(asyncio.wait(task))
