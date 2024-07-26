# -*- coding: utf-8 -*-

from wserver_infra.config.api import config


def test():
    # main.py
    _ = config
    # from rich import print as rprint
    # rprint(config)
    _ = config.env

    # app.py
    _ = config.env.s3uri_data

    _ = config.env.s3uri_acore_server_config
    _ = config.env.vpc_id
    _ = config.env.availability_zones
    _ = config.env.server_subnet_ids
    _ = config.env.db_subnet_ids
    _ = config.env.ssh_allowed_ips

    _ = config.env.s3dir_data
    _ = config.env.env_vars
    _ = config.env.devops_aws_tags
    _ = config.env.workload_aws_tags

    # deploy.py
    _ = config.env.s3uri_artifacts
    _ = config.env.s3uri_docs

    _ = config.env.s3dir_artifacts
    _ = config.env.s3dir_env_artifacts
    _ = config.env.s3dir_tmp
    _ = config.env.s3dir_config
    _ = config.env.s3dir_docs

    # name.py
    _ = config.env.cloudformation_stack_name
    _ = config.env.dynamodb_table_name_prefix

    # server.py
    _ = config.env.servers
    for name, server in config.env.servers.items():
        _ = server.id
        _ = server.play_allowed_ips

    _ = config.env.server_blue
    _ = config.env.server_green


if __name__ == "__main__":
    from wserver_infra.tests import run_cov_test

    run_cov_test(__file__, "wserver_infra.config", preview=False)
