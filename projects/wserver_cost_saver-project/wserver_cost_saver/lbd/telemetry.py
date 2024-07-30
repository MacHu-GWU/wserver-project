# -*- coding: utf-8 -*-

"""
"""

import typing as T
from ..logger import logger
from ..dynamodb import Ec2RdsStatusMeasurement
from ..config.load import config


@logger.pretty_log()
def low_level_api() -> dict:
    measurement_list: T.List[Ec2RdsStatusMeasurement] = (
        Ec2RdsStatusMeasurement.measure_on_lambda(
            server_id_list=config.env.server_id_list
        )
    )
    return {
        "measurements": [
            measurement.to_dynamodb_dict() for measurement in measurement_list
        ]
    }


def lambda_handler(event: dict, context):  # pragma: no cover
    return low_level_api()
