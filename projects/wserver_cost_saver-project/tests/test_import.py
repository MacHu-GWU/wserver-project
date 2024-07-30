# -*- coding: utf-8 -*-

import os
import pytest
import wserver_cost_saver


def test_import():
    _ = wserver_cost_saver


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
