import json
from aio_pika import Message
from src import config

from src.amqp.base import RabbitBase

class RabbitProducer(RabbitBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def start(self):
        await self.connect()
    
    async def stop(self):
        await self.disconnect()

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


rabbit_producer = RabbitProducer(
    host=config.RABBITMQ_HOST, # type: ignore
    port=config.RABBITMQ_PORT, # type: ignore
    login=config.RABBITMQ_USER, # type: ignore
    password=config.RABBITMQ_PASS, # type: ignore
)