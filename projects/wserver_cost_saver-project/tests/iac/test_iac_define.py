# -*- coding: utf-8 -*-

import json
import aws_cdk as cdk
import aws_cdk.assertions as assertions
from wserver_cost_saver.iac.define import MainStack
from wserver_cost_saver.config.api import config


def test():
    app = cdk.App()
    stack = MainStack(
        app,
        config.env.env_name,
        config=config,
        env=config.env,
        stack_name=config.env.prefix_name_slug,
    )
    for key, value in config.env.workload_aws_tags.items():
        cdk.Tags.of(app).add(key, value)
    template = assertions.Template.from_stack(stack)
    # print(json.dumps(template.to_json(), indent=4))


if __name__ == "__main__":
    from wserver_cost_saver.tests import run_cov_test

    run_cov_test(__file__, "wserver_cost_saver.iac.define", preview=False)
