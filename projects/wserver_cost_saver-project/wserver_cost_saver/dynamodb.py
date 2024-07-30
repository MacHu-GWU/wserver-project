# -*- coding: utf-8 -*-

import pynamodb_mate.api as pm
import acore_server_monitoring_measurement.api as acore_server_monitoring_measurement

from .config.load import config


class Ec2RdsStatusMeasurement(acore_server_monitoring_measurement.Ec2RdsStatusMeasurement):
    class Meta:
        table_name = config.env.measurement_dynamodb_table_name
        region = "us-east-1"
        billing_mode = pm.constants.PAY_PER_REQUEST_BILLING_MODE
