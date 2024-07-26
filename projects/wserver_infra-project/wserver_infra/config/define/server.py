# -*- coding: utf-8 -*-

"""
Todo: add docstring.
"""

import typing as T
import dataclasses


@dataclasses.dataclass
class Server:
    """
    Per Game Server infrastructure related config.

    :param id: Server id, the naming convention is ``${env_name}-${server_name}``
    :param play_allowed_ips: List of IPs allowed to play on the server.
    """

    id: T.Optional[str] = dataclasses.field(default=None)
    play_allowed_ips: T.List[str] = dataclasses.field(default_factory=list)

    @property
    def env_name(self) -> str:
        return self.id.split("-", 1)[0]

    @property
    def server_name(self) -> str:
        return self.id.split("-", 1)[1]


@dataclasses.dataclass
class ServerMixin:
    servers: T.Dict[str, Server] = dataclasses.field(default_factory=dict)

    def get_server_by_id(self, server_id: str) -> Server:  # pragma: no cover
        server_name = server_id.split("-", 1)[1]
        return self.servers[server_name]

    def get_server_by_name(self, server_name: str) -> Server:  # pragma: no cover
        return self.servers[server_name]

    @property
    def server_blue(self) -> Server:
        return self.servers["blue"]

    @property
    def server_green(self) -> Server:
        return self.servers["green"]
