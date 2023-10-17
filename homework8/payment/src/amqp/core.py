import json
import config

from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
from aio_pika import connect_robust, Message


class RabbitConnection():
    connection: AbstractRobustConnection | None = None
    channel: AbstractRobustChannel | None = None

    def status(self):
        if not self.connection or not self.channel:
            return False
        
        if self.connection.is_closed or self.channel.is_closed:
            return False
        
        return True
    
    async def _clear(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

        self.connection = None
        self.channel = None
    
    async def connect(self):
        try:
            self.connection = await connect_robust(
                host=config.RABBITMQ_HOST, # type: ignore
                port=config.RABBITMQ_PORT, # type: ignore
                login=config.RABBITMQ_USER, # type: ignore
                password=config.RABBITMQ_PASS, # type: ignore
            )
            self.channel = await self.connection.channel(publisher_confirms=False)
        except Exception as e:
            print(e)
            await self._clear()

    async def disconnect(self):
        await self._clear()

    async def send_message(
        self,
        messages: list | dict,
        routing_key: str
    ):
        if not self.channel:
            raise RuntimeError("Rabbit not connected")
        
        if isinstance(messages, dict):
            messages = [messages]
        
        async with self.channel.transaction():
            for message in messages:
                message = Message(
                    body=json.dumps(message).encode()
                )

                await self.channel.default_exchange.publish(
                    message=message,
                    routing_key=routing_key
                )


rabbit_connection = RabbitConnection()