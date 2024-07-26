# -*- coding: utf-8 -*-

import json
from urllib import request
from boto_session_manager import BotoSesManager

from .define.api import Env

url = "https://checkip.amazonaws.com"


def get_public_ip() -> str:
    with request.urlopen(url) as response:
        return response.read().decode("utf-8").strip()


def put_ip_white_list(env: "Env", bsm: BotoSesManager):
    """
    Put the latest ip white list to S3.
    """
    ip_white_list = [
        get_public_ip(),
    ]
    env.s3path_ip_white_list_json.write_text(
        json.dumps(ip_white_list, indent=4, sort_keys=True),
        bsm=bsm,
        content_type="application/json",
    )
