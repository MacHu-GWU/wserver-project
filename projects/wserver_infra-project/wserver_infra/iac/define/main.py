# -*- coding: utf-8 -*-

"""
This module is the CloudFormation stack definition.
"""

import aws_cdk as cdk
from constructs import Construct

from ...config.define.api import Env, Config
from ...git import git_repo

from .iam import IamMixin
from .vpc import VpcMixin
from .rds import RdsMixin


class MainStack(
    cdk.Stack,
    IamMixin,
    VpcMixin,
    RdsMixin,
):
    """
    A Python class wrapper around the real CloudFormation stack, to provide
    attribute access to different AWS Resources.

    :param env: the ``Env`` object in config definition. it is used to derive
        a lot of value for AWS resources.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: Config,
        env: Env,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.config = config
        self.env = env
        self.mk_rg1_iam()
        self.mk_rg2_vpc()
        self.mk_rg3_rds()

        for key, value in config.env.workload_aws_tags.items():
            cdk.Tags.of(self).add(key, value)

        cdk.Tags.of(self).add("tech:git_commit_id", git_repo.git_commit_id)
        cdk.Tags.of(self).add("tech:git_repo_name", "wserver-project")
