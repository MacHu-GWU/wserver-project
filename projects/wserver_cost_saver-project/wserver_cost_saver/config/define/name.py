# -*- coding: utf-8 -*-

import typing as T
import dataclasses

if T.TYPE_CHECKING:  # pragma: no cover
    from .main import Env


@dataclasses.dataclass
class NameMixin:
    @property
    def measurement_dynamodb_table_name(self: "Env") -> str:
        return f"wserver_infra-{self.env_name}-server_monitoring"
