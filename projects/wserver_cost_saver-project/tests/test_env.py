# -*- coding: utf-8 -*-

from wserver_cost_saver.env import EnvNameEnum, detect_current_env


def test():
    _ = detect_current_env()


if __name__ == "__main__":
    from wserver_cost_saver.tests import run_cov_test

    run_cov_test(__file__, "wserver_cost_saver.env", preview=False)
