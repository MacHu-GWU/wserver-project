# -*- coding: utf-8 -*-

import moto
from wserver_cost_saver.logger import logger
from wserver_cost_saver.config.api import config
from wserver_cost_saver.lbd.s3sync import low_level_api
from wserver_cost_saver.tests.mock import BaseMockTest


class Test(BaseMockTest):
    mock_list = [
        moto.mock_s3,
    ]
    s3path_source = None
    s3path_target = None

    @classmethod
    def setup_class_post_hook(cls):
        cls.bsm.s3_client.create_bucket(Bucket=config.env.s3dir_data.bucket)

        cls.s3path_source = config.env.s3dir_source.joinpath("file.txt")
        cls.s3path_target = config.env.s3dir_target.joinpath("file.txt")
        cls.s3path_source.write_text("hello")

    def _test_low_level_api(self):
        assert self.s3path_source.exists() is True
        assert self.s3path_target.exists() is False

        low_level_api(s3path_source=self.s3path_source)
        assert self.s3path_target.exists() is True
        assert self.s3path_target.read_text() == "hello"

    def test_low_level_api(self):
        with logger.disabled(
            disable=True,
            # disable=False,
        ):
            self._test_low_level_api()


if __name__ == "__main__":
    from wserver_cost_saver.tests import run_cov_test

    run_cov_test(__file__, "wserver_cost_saver.lbd.s3sync", preview=False)
