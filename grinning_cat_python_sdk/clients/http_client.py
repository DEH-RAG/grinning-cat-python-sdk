from requests_toolbelt.sessions import BaseUrlSession
from urllib.parse import urlunparse
from typing import Callable, List


class HttpClient:
    def __init__(
        self,
        host: str,
        port: int | None = None,
        apikey: str | None = None,
        is_https: bool = False
    ):
        self.host = host
        self.port = port
        self.apikey = apikey
        self.token = None
        self.agent_id = None
        self.user_id = None
        self.chat_id = None
        self.is_https = is_https
        self.headers = {}

        self.middlewares: List[Callable] = [
            self.__before_secure_request,
            self.__before_jwt_request,
        ]

    def set_token(self, token: str):
        self.token = token
        return self

    def get_http_uri(self) -> str:
        scheme = "https" if self.is_https else "http"
        netloc = f"{self.host}:{self.port}" if self.port else self.host

        return urlunparse((scheme, netloc, "", "", "", ""))

    def _set_or_drop_header(self, name: str, value: str | None) -> None:
        """Set the header when a value is provided, otherwise drop any stale value.

        `self.headers` is reused across calls, so a previous value would leak
        into the next request when the new call passes ``None`` for the same
        identifier (agent_id / user_id / chat_id).
        """
        if value:
            self.headers[name] = value
        else:
            self.headers.pop(name, None)

    def __before_secure_request(self):
        if self.apikey:
            self.headers["Authorization"] = f"Bearer {self.apikey}"
        self._set_or_drop_header("X-Agent-ID", self.agent_id)
        self._set_or_drop_header("X-User-ID", self.user_id)
        self._set_or_drop_header("X-Chat-ID", self.chat_id)

    def __before_jwt_request(self):
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"
        self._set_or_drop_header("X-Agent-ID", self.agent_id)
        self._set_or_drop_header("X-Chat-ID", self.chat_id)

    def get_client(
        self,
        agent_id: str | None = None,
        user_id: str | None = None,
        chat_id: str | None = None,
    ) -> BaseUrlSession:
        if not self.apikey and not self.token:
            raise ValueError("You must provide an apikey or a token")

        # Reset header dict each call so stale values from a previous
        # request cannot leak into the next session.
        self.headers = {}
        self.agent_id = agent_id
        self.user_id = user_id
        self.chat_id = chat_id

        for middleware in self.middlewares:
            middleware()

        return self.get_base_session()

    def get_base_session(self) -> BaseUrlSession:
        session = BaseUrlSession(base_url=self.get_http_uri())
        session.headers = self.headers

        return session
