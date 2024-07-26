Wserver AWS Infrastructure Walkthrough
==============================================================================


Overview
------------------------------------------------------------------------------
wserver 这个项目下有很多子项目. 而 wserver_infra 项目是为了部署那些子项目共享的的 AWS 资源. 如果某个资源只会在一个子项目中用到, 那么不要在 wserver_infra 的 CDK stack 中定义, 而要在该子项目中定义.


Resource List
------------------------------------------------------------------------------
- `IAM Roles <https://github.com/MacHu-GWU/wserver-project/blob/wserver_infra/feature/projects/wserver_infra-project/wserver_infra/iac/define/iam.py>`_
    - ``iam_role_for_ec2``: EC2 IAM profile.
- `Security Groups <https://github.com/MacHu-GWU/wserver-project/blob/wserver_infra/feature/projects/wserver_infra-project/wserver_infra/iac/define/vpc.py>`_
    - ``sg_list_default``: default security group for the current environment, all of the resources in this environment should have this security group, so they can talk to each other.
    - ``sg_list_ec2``: security group for EC2 instances.
    - ``sg_list_ssh``: security group for SSH access.
- `RDS <https://github.com/MacHu-GWU/wserver-project/blob/wserver_infra/feature/projects/wserver_infra-project/wserver_infra/iac/define/rds.py>`_:
    - ``private_db_subnet_group``: private subnet group for RDS.
