Maintainer Home IP
==============================================================================
在我们这个项目中我们的游戏服务器不是对全世界开放的, 而是只对 IP 白名单中的人开放.

当然作为项目维护者自己的 IP 是一定要加入白名单的. 这里由于我家没有静态 IP 所以我写了个 :func:`脚本 <wserver_infra.ops.deploy_app>`, 在每次从 local laptop deploy CDK 的时候就会把自己最新的 IP 地址上传到所有环境中的 S3 bucket 中 (devops, sbx, tst, prd). 然后在 CDK 的脚本里会去 S3 上获取最新的 IP 地址, 并且更新到对应的 security group 中.

而对于其他的 IP 地址, 例如想要在我的服务器上玩的小伙伴, 那么我会获得它们的 IP 地址并将其放入 `config.json <https://github.com/MacHu-GWU/wserver-project/blob/wserver_infra/feature/projects/wserver_infra-project/config/config.json>`_ 中的 ``*.servers.*.play_allowed_ips`` 的列表中.

而如果我还有其他的办公场所的 IP 地址也需要加入到白名单, 我会将这些 IP 地址放入 ``*.ssh_allowed_ips`` 的列表中.
