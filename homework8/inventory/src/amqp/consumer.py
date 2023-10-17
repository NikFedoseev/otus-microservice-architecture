from src.amqp.base import RabbitBase

class RabbitConsumer(RabbitBase):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    async def start(self):
        await self.connect()
    
    async def stop(self):
        await self.disconnect()
