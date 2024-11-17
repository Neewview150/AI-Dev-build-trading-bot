import asyncio
import websockets
import logging
from .config import load_config

class ChatHandler:
    def __init__(self):
        self.config = load_config()
        self.server_address = self.config.get('chat_server_address', 'ws://localhost:8765')
        self.logger = logging.getLogger('ChatHandler')

    async def connect(self):
        try:
            self.connection = await websockets.connect(self.server_address)
            self.logger.info(f"Connected to chat server at {self.server_address}")
        except Exception as e:
            self.logger.error(f"Failed to connect to chat server: {e}")

    async def send_message(self, message: str):
        try:
            await self.connection.send(message)
            self.logger.info(f"Sent message: {message}")
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")

    async def receive_message(self):
        try:
            message = await self.connection.recv()
            self.logger.info(f"Received message: {message}")
            return message
        except Exception as e:
            self.logger.error(f"Failed to receive message: {e}")
            return None

    async def run(self):
        await self.connect()
        while True:
            message = await self.receive_message()
            if message:
                # Handle incoming message
                pass

# Example usage
if __name__ == "__main__":
    chat_handler = ChatHandler()
    asyncio.run(chat_handler.run())
