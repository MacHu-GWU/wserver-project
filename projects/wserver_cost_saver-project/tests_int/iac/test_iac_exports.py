# -*- coding: utf-8 -*-

import os
import pytest

from wserver_cost_saver.boto_ses import bsm
from wserver_cost_saver.iac.exports import StackExports
from wserver_cost_saver.config.load import config


class TestStackExports:
    def test(self):
        stack_exports = StackExports(env_name=config.env.env_name)
        stack_exports.load(bsm.cloudformation_client)
        _ = stack_exports.get_iam_role_for_lambda_arn()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
