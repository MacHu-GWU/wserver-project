# -*- coding: utf-8 -*-

from wserver_infra.env import EnvNameEnum, detect_current_env


def test():
    _ = detect_current_env()


if __name__ == "__main__":
    from wserver_infra.tests import run_cov_test

    run_cov_test(__file__, "wserver_infra.env", preview=False)
