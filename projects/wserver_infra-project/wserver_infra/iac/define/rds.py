# -*- coding: utf-8 -*-

import typing as T

import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
)

if T.TYPE_CHECKING:
    from .main import MainStack


class RdsMixin:
    def mk_rg3_rds(self: "MainStack"):
        """
        - DB subnet group.
        """
        subnet_group_description = "DB Subnet Group for VPC accessible DB"
        self.private_db_subnet_group = rds.SubnetGroup(
            self,
            "DBSubnetGroupForPrivateDB",
            vpc=self.vpc,
            subnet_group_name=f"{self.env.prefix_name_slug}-db",
            description=subnet_group_description,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[
                    ec2.Subnet.from_subnet_id(
                        self,
                        f"Subnet-{subnet_id}",
                        subnet_id,
                    )
                    for subnet_id in self.env.db_subnet_ids
                ],
            ),
        )

        output_sg_ssh_id = cdk.CfnOutput(
            self,
            f"OutputDBSubnetGroupNameForPrivateDB",
            description=subnet_group_description,
            value=self.private_db_subnet_group.subnet_group_name,
            export_name=f"{self.env.prefix_name_slug}-db-subnet-group-name-for-private-db",
        )
        self.sg_output_list_ssh.append(output_sg_ssh_id)
