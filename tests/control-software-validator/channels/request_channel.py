from typing import Any

from pydantic import BaseModel
from typing_extensions import override
from zmq.asyncio import Socket


class RequestChannel:
    def __init__(self, stream: Socket) -> None:
        self.stream = stream

    def connect(self, address: str) -> None:
        self.stream.connect(address)

    async def request(self, request: BaseModel, return_type: type[BaseModel]) -> Any:
        # Serializes request and tests if response is correctly formatted
        self.stream.send_string(request.model_dump_json())
        reply = await self.stream.recv_string()
        return return_type.model_validate_json(reply)


class MockRequestChannel(RequestChannel):
    @override
    async def request(self, request: BaseModel, return_type: type[BaseModel]) -> Any:
        # Only serializes request but does not actually send it
        _ = request.model_dump_json()
        return None
