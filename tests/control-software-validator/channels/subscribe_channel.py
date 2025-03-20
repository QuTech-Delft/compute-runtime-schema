from typing import Any

from typing_extensions import override
from zmq.asyncio import Socket


class SubscribeChannel:
    def __init__(self, stream: Socket) -> None:
        self.stream = stream

    def connect(self, address: str) -> None:
        self.stream.connect(address)
        self.stream.subscribe("")

    async def receive(self, return_type: Any) -> Any:
        reply = await self.stream.recv_string()
        return return_type.model_validate_json(reply)


class MockSubscribeChannel(SubscribeChannel):
    @override
    async def receive(self, return_type: Any) -> Any:
        # Does not actually receive anything
        return None
