# -*- coding: utf-8 -*-

import os
import pytest

from wserver_infra.boto_ses import bsm
from wserver_infra.iac.exports import StackExports
from wserver_infra.config.load import config


class TestStackExports:
    def test(self):
        stack_exports = StackExports(env_name=config.env.env_name)
        stack_exports.load(bsm.cloudformation_client)
        _ = stack_exports.get_iam_managed_policy_dummy_arn()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
