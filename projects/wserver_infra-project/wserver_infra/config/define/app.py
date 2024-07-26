# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from s3pathlib import S3Path

from ..._version import __version__

if T.TYPE_CHECKING:  # pragma: no cover
    from .main import Env


@dataclasses.dataclass
class AppMixin:
    """
    :param vpc_id: use which VPC to host the wow server fleet
    :param server_subnet_ids: use which subnets to host the game server
        (has to be public subnet)
    :param db_subnet_ids: use which subnets to host the database
        (has to be private subnet)
    :param ssh_allowed_ips: allow which IPs to SSH into the game server
    """
    s3uri_acore_server_config: T.Optional[str] = dataclasses.field(default=None)
    vpc_id: T.Optional[str] = dataclasses.field(default=None)
    availability_zones: T.List[str] = dataclasses.field(default_factory=list)
    server_subnet_ids: T.List[str] = dataclasses.field(default_factory=list)
    db_subnet_ids: T.List[str] = dataclasses.field(default_factory=list)
    ssh_allowed_ips: T.List[str] = dataclasses.field(default_factory=list)

    @property
    def s3dir_acore_server_config(self) -> S3Path:
        """
        Where we store acore server config data in S3?
        """
        return S3Path.from_s3_uri(self.s3uri_acore_server_config).to_dir()

    @property
    def s3path_ip_white_list_json(self: "Env") -> S3Path:
        return self.s3dir_env_data.joinpath("ip_white_list.json")

    @property
    def dynamodb_table_name_prefix(self: "Env") -> str:
        """
        All DynamoDB table name should start with this prefix.
        """
        return self.prefix_name_snake

    @property
    def env_vars(self: "Env") -> T.Dict[str, str]:
        """
        Common environment variable for all computational resources in this environment.
        It is primarily for "self awareness" (detect who I am, which environment I am in).
        """
        env_vars = super().env_vars
        env_vars["PACKAGE_VERSION"] = __version__
        return env_vars

    @property
    def devops_aws_tags(self: "Env") -> T.Dict[str, str]:
        """
        Common AWS resources tags for all resources in devops environment.
        """
        tags = super().devops_aws_tags
        tags["tech:package_version"] = __version__
        return tags

    @property
    def workload_aws_tags(self: "Env") -> T.Dict[str, str]:
        """
        Common AWS resources tags for all resources in workload environment.
        """
        tags = super().workload_aws_tags
        tags["tech:package_version"] = __version__
        return tags
