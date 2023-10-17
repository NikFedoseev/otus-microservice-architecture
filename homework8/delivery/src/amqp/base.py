import asyncio

from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
from aio_pika import connect_robust

MAX_CONNECT_RETRIES = 10


class RabbitBase():
    connection: AbstractRobustConnection | None = None
    channel: AbstractRobustChannel | None = None

    def __init__(
            self,
            host,
            port,
            login,
            password,
            max_conntect_retries = MAX_CONNECT_RETRIES,
            loop = None
        ) -> None:
        self.max_connect_retries = max_conntect_retries
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.loop = loop

    def status(self):
        if not self.connection or not self.channel:
            return False
        
        if self.connection.is_closed or self.channel.is_closed:
            return False
        
        return True
    
    
    async def connect(self):
        for retry in range(self.max_connect_retries):
            try:
                self.connection = await connect_robust(
                    host=self.host, # type: ignore
                    port=self.port, # type: ignore
                    login=self.login, # type: ignore
                    password=self.password, # type: ignore
                    loop=self.loop
                )
                self.channel = await self.connection.channel(publisher_confirms=False)
                return
            except Exception as e:
                print("ERROR")
                await self.disconnect()
                await asyncio.sleep(1)

    async def disconnect(self):
        print("DISCONNECT")
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

        self.connection = None
        self.channel = None

