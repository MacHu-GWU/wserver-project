# -*- coding: utf-8 -*-

from wserver_cost_saver.git import git_repo


def test():
    _ = git_repo.git_branch_name
    _ = git_repo.semantic_branch_name


if __name__ == "__main__":
    from wserver_cost_saver.tests import run_cov_test

    run_cov_test(__file__, "wserver_cost_saver.git", preview=False)
