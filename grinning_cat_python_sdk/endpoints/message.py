from typing import Callable
import json

from grinning_cat_python_sdk.endpoints.base import AbstractEndpoint
from grinning_cat_python_sdk.models.api.messages import ChatOutput
from grinning_cat_python_sdk.models.dtos import Message
from grinning_cat_python_sdk.utils import deserialize


class MessageEndpoint(AbstractEndpoint):
    def send_http_message(
        self,
        message: Message,
        agent_id: str,
        user_id: str,
        chat_id: str | None = None,
    ) -> ChatOutput:
        """
        This endpoint sends a message to the agent identified by the agentId parameter. The message is sent via HTTP.
        :param message: Message object, the message to send
        :param agent_id: the agent id
        :param user_id: the user id
        :param chat_id: the chat id (optional)
        :return: ChatOutput object
        """
        return self.post_json(
            '/message',
            agent_id,
            output_class=ChatOutput,
            payload=message.model_dump(),
            user_id=user_id,
            chat_id=chat_id,
        )

    async def send_websocket_message(
        self,
        message: Message,
        agent_id: str,
        user_id: str,
        chat_id: str | None = None,
        callback: Callable[[dict], None] | None = None,
    ) -> ChatOutput:  # type: ignore
        """
        This endpoint sends a message to the agent identified by the agentId parameter. The message is sent via WebSocket.
        :param message: Message object, the message to send
        :param agent_id: the agent id
        :param user_id: the user id
        :param chat_id: the chat id
        :param callback: callable, a callback function that will be called for each message received
        :return: ChatOutput object
        """
        try:
            json_data = json.dumps(message.model_dump())
        except Exception:
            raise RuntimeError("Error encoding message")

        client = await self.get_ws_client(agent_id, user_id, chat_id)

        try:
            await client.send(json_data)

            while True:
                raw_response = await client.recv()

                if raw_response == "ping":
                    await client.send("pong")
                    continue

                if raw_response == "pong":
                    continue

                response = json.loads(raw_response)
                response_type = response.get("type")
                if response_type != "chat":
                    if callback:
                        callback(response)
                    continue

                return deserialize(json.loads(response["content"]), ChatOutput)
        except Exception as e:
            await client.close()
            raise Exception(f"WebSocket error: {str(e)}")
        finally:
            await client.close()
