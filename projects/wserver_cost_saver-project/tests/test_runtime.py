# -*- coding: utf-8 -*-

from wserver_cost_saver.runtime import runtime


def test():
    _ = runtime


if __name__ == "__main__":
    from wserver_cost_saver.tests import run_cov_test

    run_cov_test(__file__, "wserver_cost_saver.runtime", preview=False)
