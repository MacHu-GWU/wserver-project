Centralized Multi Environment Config Management
==============================================================================


Config Management Related Modules
------------------------------------------------------------------------------
Below are the list of important files related to config management::

    wserver_cost_saver/config # the root folder of the config management system source code
    wserver_cost_saver/config/define # config schema definition
    wserver_cost_saver/config/define/main.py # centralized config object, config fields are break down into sub-modules
    wserver_cost_saver/config/define/app.py # app related configs, e.g. app name, app artifacts S3 bucket
    wserver_cost_saver/config/define/lbd_deploy.py # Lambda function deployment related configs
    wserver_cost_saver/config/define/lbd_func.py # per Lambda function name, memory size, timeout configs
    wserver_cost_saver/config/load.py # config value initialization
    config/config.json # include the non-sensitive config data
    ${HOME}/.projects/wserver_cost_saver/config-secret.json # include the sensitive config data, the ${HOME} is your user home directory
    tests/config/test_config_init.py # the unit test for config management, everytime you changed any of the config.json, or config/ modules, you should run this test


Config Schema Declaration
------------------------------------------------------------------------------
The ``wserver_cost_saver/config/define/`` module defines the configuration data schema (field and value pairs).

- To improve maintainability, we break down the long list of configuration fields into sub-modules.
- There are two types of configuration values: constant values and derived values. Constant values are static values that are hardcoded in the ``config.json`` file, typically a string or an integer. Derived values are calculated dynamically based on one or more constant values.


Config Loading
------------------------------------------------------------------------------
The ``wserver_cost_saver/config/load.py`` module defines how to read the configuration data from external storage.


Update Config Module Workflow
------------------------------------------------------------------------------
todo
