# -*- coding: utf-8 -*-

import typing as T
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

        self.stat_parameter_store = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ssm:GetParameter"],
            resources=[
                f"arn:aws:ssm:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:parameter/{self.env.parameter_name}"
            ],
        )

        self.stat_s3_bucket_read = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "s3:ListBucket",
                "s3:GetObject",
                "s3:GetObjectAttributes",
                "s3:GetObjectTagging",
            ],
            resources=[
                f"arn:aws:s3:::{self.env.s3dir_env_data.bucket}",
                f"arn:aws:s3:::{self.env.s3dir_env_data.bucket}/{self.env.s3dir_data.key}*",
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
                f"arn:aws:s3:::{self.env.s3dir_env_data.bucket}",
                f"arn:aws:s3:::{self.env.s3dir_env_data.bucket}/{self.env.s3dir_data.key}*",
            ],
        )

        self.stat_dynamodb = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "dynamodb:DescribeTable",
                "dynamodb:BatchWriteItem",
                "dynamodb:Query",
            ],
            resources=[
                f"arn:aws:dynamodb:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:table/{self.env.measurement_dynamodb_table_name}",
            ],
        )

        self.stat_list_resources = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "ec2:DescribeInstances",
                "rds:DescribeDBInstances",
            ],
            resources=[
                "*",
            ],
        )

        self.stat_start_stop_delete_computational_resources = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                # ec2 stuff
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:TerminateInstances",
                # rds stuff
                "rds:StartDBInstance",
                "rds:StopDBInstance",
                "rds:StopDBInstance",
                "rds:DeleteDBInstance",
                # ssm run command stuff
                "ssm:SendCommand",
                "ssm:GetCommandInvocation",
            ],
            resources=[
                "*",
            ],
            conditions={
                "StringEquals": {"aws:ResourceTag/wserver:env_name": self.env.env_name}
            },
        )

        # declare iam role
        self.iam_role_for_lambda = iam.Role(
            self,
            "IamRoleForLambda",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name=f"{self.env.prefix_name_snake}-{cdk.Aws.REGION}-lambda",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                ),
            ],
            inline_policies={
                f"{self.env.prefix_name_snake}-{cdk.Aws.REGION}-lambda": iam.PolicyDocument(
                    statements=[
                        self.stat_parameter_store,
                        self.stat_s3_bucket_read,
                        self.stat_s3_bucket_write,
                        self.stat_dynamodb,
                        self.stat_list_resources,
                        self.stat_start_stop_delete_computational_resources,
                    ]
                )
            },
        )

        self.output_iam_role_for_lambda_arn = cdk.CfnOutput(
            self,
            "IamRoleForLambdaArn",
            value=self.iam_role_for_lambda.role_arn,
            export_name=f"{self.env.prefix_name_slug}-lambda-role-arn",
        )
