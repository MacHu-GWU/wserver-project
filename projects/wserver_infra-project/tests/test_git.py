# -*- coding: utf-8 -*-

from wserver_infra.git import git_repo


def test():
    _ = git_repo.git_branch_name
    _ = git_repo.semantic_branch_name


if __name__ == "__main__":
    from wserver_infra.tests import run_cov_test

    run_cov_test(__file__, "wserver_infra.git", preview=False)
