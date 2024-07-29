# -*- coding: utf-8 -*-

import typing as T

import aws_cdk
import aws_cdk as cdk

from aws_cdk import (
    aws_iam as iam,
)

if T.TYPE_CHECKING:  # pragma: no cover
    from .main import MainStack


class IamMixin:
    def mk_rg1_iam(self: "MainStack"):
        """
        IAM related resources.

        Ref:

        - IAM Object quotas: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entities
        """
        # access the parameter store to get config data
        self.stat_parameter_store = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ssm:GetParameter"],
            resources=[
                f"arn:aws:ssm:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:parameter/{self.env.parameter_name}"
            ],
        )

        self.stat_iam_list_account_allias = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["iam:ListAccountAliases"],
            resources=["*"],
        )

        # read from certain S3 bucket
        self.stat_s3_bucket_get_versioning = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:GetBucketVersioning",
            ],
            resources=[
                f"arn:aws:s3:::{self.env.s3dir_acore_server_config.bucket}",
            ],
        )

        self.stat_s3_bucket_read = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:ListBucket",
                "s3:GetObject",
                "s3:GetObjectAttributes",
                "s3:GetObjectTagging",
                "s3:GetBucketVersioning",
            ],
            resources=[
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}",
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}/{self.env.s3dir_data.key}*",
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}/projects/acore_*",
                f"arn:aws:s3:::{self.env.s3dir_acore_server_config.bucket}",
                f"arn:aws:s3:::{self.env.s3dir_acore_server_config.bucket}/{self.env.s3dir_acore_server_config.key}*",
            ],
        )

        self.stat_s3_bucket_write = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:PutObjectTagging",
                "s3:DeleteObjectTagging",
            ],
            resources=[
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}",
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}/{self.env.s3dir_data.key}*",
                f"arn:aws:s3:::{self.env.s3dir_data.bucket}/projects/acore_*",
            ],
        )

        # be able to get caller identity, describe ec2 and rds instances
        self.stat_sts_ec2_rds = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "sts:GetCallerIdentity",
                "ec2:DescribeInstances",
                "ec2:CreateTags",
                "rds:DescribeDBInstances",
            ],
            resources=["*"],
        )

        self.stat_sts_ec2_rds = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "sts:GetCallerIdentity",
                "ec2:DescribeInstances",
                "ec2:CreateTags",
                "rds:DescribeDBInstances",
            ],
            resources=["*"],
        )

        self.stat_dynamodb = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["dynamodb:PutItem", "dynamodb:DescribeTable"],
            resources=[
                f"arn:aws:dynamodb:{aws_cdk.Aws.REGION}:{aws_cdk.Aws.ACCOUNT_ID}:table/{self.env.dynamodb_table_name_prefix}*"
            ],
        )

        # declare iam role
        iam_role_description = (
            f"shared IAM role for all EC2 instances in {self.env.env_name}"
        )
        self.iam_role_for_ec2 = iam.Role(
            self,
            "IamRoleForEC2",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            role_name=f"{self.env.prefix_name_snake}-{cdk.Aws.REGION}-ec2",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonEC2ReadOnlyAccess"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
            ],
            inline_policies={
                f"{self.env.prefix_name_snake}-{cdk.Aws.REGION}-ec2": iam.PolicyDocument(
                    statements=[
                        # EC2 instance need to get parameter from parameter store
                        self.stat_parameter_store,
                        # EC2 instance need to get account alias
                        self.stat_iam_list_account_allias,
                        # EC2 instance need to check if the config s3 bucket turned version on
                        self.stat_s3_bucket_get_versioning,
                        self.stat_s3_bucket_read,
                        self.stat_s3_bucket_write,
                        # EC2 instance need to be able to get caller identity
                        # EC2 instance need to be able to put tag to EC2
                        self.stat_sts_ec2_rds,
                        # EC2 instance need to write server measurement data to DynamoDB
                        self.stat_dynamodb,
                    ]
                )
            },
            description=iam_role_description,
        )

        self.output_iam_role_for_ec2_arn = cdk.CfnOutput(
            self,
            "IamRoleForEC2Arn",
            description=iam_role_description,
            value=self.iam_role_for_ec2.role_arn,
            export_name=f"{self.env.prefix_name_slug}-ec2-iam-role-arn",
        )

        self.instance_profile = iam.CfnInstanceProfile(
            self,
            "InstanceProfileForEC2",
            roles=[self.iam_role_for_ec2.role_name],
            instance_profile_name=f"{self.env.prefix_name_snake}-{cdk.Aws.REGION}-ec2",
        )

        self.output_instance_profile_arn = cdk.CfnOutput(
            self,
            "InstanceProfileForEC2Arn",
            description=iam_role_description,
            value=self.instance_profile.attr_arn,
            export_name=f"{self.env.prefix_name_slug}-instance-profile-arn",
        )
