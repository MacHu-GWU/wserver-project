# -*- coding: utf-8 -*-

import os
import pytest
import wserver_infra


def test_import():
    _ = wserver_infra


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
