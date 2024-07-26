# -*- coding: utf-8 -*-

import typing as T
import json

import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
)

from ...config.define.server import Server
from ...boto_ses import bsm

if T.TYPE_CHECKING:  # pragma: no cover
    from .main import MainStack


class VpcMixin:
    def create_default_sg(self: "MainStack", server: Server):
        """
        1. default security group.
        """
        sg_name = f"{self.env.prefix_name_snake}/sg/{server.id}-default"

        sg_default_logic_id = f"SecurityGroup-{server.id}-Default"
        sg_default_desription = (
            "allow all traffic from the same SG, "
            "each server and corresponding RDS instance should have this SG"
        )
        sg_default = ec2.SecurityGroup(
            self,
            sg_default_logic_id,
            description=sg_default_desription,
            security_group_name=sg_name,
            vpc=self.vpc,
        )
        cdk.Tags.of(sg_default).add("Name", sg_name)
        self.sg_list_default.append(sg_default)

        output_sg_default_id = cdk.CfnOutput(
            self,
            f"Output{sg_default_logic_id}Id",
            description=sg_default_desription,
            value=sg_default.security_group_id,
            export_name=f"{self.env.prefix_name_slug}-{server.id}-sg-default-id",
        )
        self.sg_output_list_default.append(output_sg_default_id)

        sg_default.add_ingress_rule(
            peer=sg_default,
            connection=ec2.Port.all_traffic(),
            description="Allow all traffic from the same security group",
        )

    def create_ec2_sg(self: "MainStack", server: Server):
        """
        2. server security group.

        authserver use port 3724, and worldserver use port 8085.

        Reference:

        - https://www.azerothcore.org/wiki/networking
        """
        sg_name = f"{self.env.prefix_name_snake}/sg/{server.id}-ec2"

        sg_ec2_logic_id = f"SecurityGroup-{server.id}-EC2"
        sg_ec2_description = "For authserver and worldserver TCP and UDP only"
        sg_ec2 = ec2.SecurityGroup(
            self,
            sg_ec2_logic_id,
            description=sg_ec2_description,
            security_group_name=sg_name,
            vpc=self.vpc,
        )
        cdk.Tags.of(sg_ec2).add("Name", sg_name)
        self.sg_list_ec2.append(sg_ec2)

        output_sg_ec2_id = cdk.CfnOutput(
            self,
            f"Output{sg_ec2_logic_id}Id",
            description=sg_ec2_description,
            value=sg_ec2.security_group_id,
            export_name=f"{self.env.prefix_name_slug}-{server.id}-sg-ec2-id",
        )
        self.sg_output_list_ec2.append(output_sg_ec2_id)
        AUTH_SERVER_PORT = 3724
        WORLD_SERVER_PORT = 8085
        args = [
            ("auth", "tpc", ec2.Port.tcp(AUTH_SERVER_PORT)),
            ("auth", "udp", ec2.Port.udp(AUTH_SERVER_PORT)),
            ("world", "tpc", ec2.Port.tcp(WORLD_SERVER_PORT)),
            ("world", "udp", ec2.Port.udp(WORLD_SERVER_PORT)),
        ]

        ip_white_list = json.loads(self.env.s3path_ip_white_list_json.read_text(bsm=bsm))

        for auth_name, protocol, connection in args:
            # if we don't restrict which IP can play on this server, we allow all traffic
            play_allowed_ips = ip_white_list + server.play_allowed_ips
            if len(play_allowed_ips) == 0:
                sg_ec2.add_ingress_rule(
                    peer=ec2.Peer.any_ipv4(),
                    connection=connection,
                    description=f"{auth_name.title()} Server",
                )
            else:
                # grant specific IP to play on this server
                for ip in server.play_allowed_ips:
                    sg_ec2.add_ingress_rule(
                        peer=ec2.Peer.ipv4(f"{ip}/32"),
                        connection=connection,
                        description=f"{auth_name.title()} Server",
                    )

    def create_ssh_sg(self: "MainStack"):
        """
        3. ssh sg.
        """
        sg_name = f"{self.env.prefix_name_snake}/sg/ssh"

        sg_ssh_logic_id = f"SecurityGroup-SSH"
        sg_ssh_description = (
            "Allow restricted development traffic from authorized ip, "
            "usually workspace ip or developer home ip"
        )
        sg_ssh = ec2.SecurityGroup(
            self,
            sg_ssh_logic_id,
            description=sg_ssh_description,
            security_group_name=sg_name,
            vpc=self.vpc,
        )
        cdk.Tags.of(sg_ssh).add("Name", sg_name)
        self.sg_ssh = sg_ssh

        output_sg_ssh_id = cdk.CfnOutput(
            self,
            f"Output{sg_ssh_logic_id}Id",
            description=sg_ssh_description,
            value=sg_ssh.security_group_id,
            export_name=f"{self.env.prefix_name_slug}-sg-ssh-id",
        )
        self.sg_output_list_ssh.append(output_sg_ssh_id)

        # grant specific IP to SSH to this server
        ip_white_list = json.loads(self.env.s3path_ip_white_list_json.read_text(bsm=bsm))

        for ip in (ip_white_list + self.env.ssh_allowed_ips):
            sg_ssh.add_ingress_rule(
                peer=ec2.Peer.ipv4(f"{ip}/32"),
                connection=ec2.Port.tcp(22),
                description=sg_ssh_description,
            )

    def mk_rg2_vpc(self: "MainStack"):
        """
        - one security group for this environment to allow SSH access to game server
        - per server security group to allow player to play on the specific game server
        - per server security group to allow game server talking to database
        """
        self.vpc = ec2.Vpc.from_vpc_attributes(
            self,
            "Vpc",
            vpc_id=self.env.vpc_id,
            availability_zones=[
                "us-east-1a",
                "us-east-1b",
                "us-east-1c",
            ]
        )
        self.sg_list_default: T.List[ec2.SecurityGroup] = list()
        self.sg_output_list_default: T.List[cdk.CfnOutput] = list()

        self.sg_list_ec2: T.List[ec2.SecurityGroup] = list()
        self.sg_output_list_ec2: T.List[cdk.CfnOutput] = list()

        self.sg_list_ssh: T.List[ec2.SecurityGroup] = list()
        self.sg_output_list_ssh: T.List[cdk.CfnOutput] = list()

        for name, server in self.env.servers.items():
            self.create_default_sg(server)
            self.create_ec2_sg(server)

        self.create_ssh_sg()
