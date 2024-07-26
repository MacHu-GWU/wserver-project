Welcome to ``wserver_infra`` Documentation
==============================================================================
这个项目负责部署 wserver 项目的 AWS infrastructure resource. 主要是一些网络资源, 例如 IAM Role, Security Group, DB Subnet Group 等.

For first time user, please run the following command to build project documentation website and read it::

    # create virtualenv
    make venv-create

    # install all dependencies
    make install-all

    # build documentation website locally
    make build-doc

    # view documentation website in browser
    make view-doc
