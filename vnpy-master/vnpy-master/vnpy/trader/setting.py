"""
Global setting of the trading platform.
"""

from logging import INFO
from tzlocal import get_localzone_name

from .utility import load_json


SETTINGS: dict = {
    "font.family": "微软雅黑",
    "font.size": 12,

    "log.active": True,
    "log.level": INFO,
    "log.console": True,
    "log.file": True,

    "email.server": "smtp.qq.com",
    "email.port": 465,
    "email.username": "",
    "email.password": "",
    "email.sender": "",
    "email.receiver": "",

    "datafeed.name": "",
    "datafeed.username": "",
    "datafeed.password": "",

    "database.timezone": get_localzone_name(),
    "database.name": "sqlite",
    "database.database": "C://Users//iamwu//.vntrader//database.db",
    "database.host": "localhost",
    "database.port": 0,
    "database.user": "",
    "database.password": ""

    # "database.timezone": get_localzone_name(),
    # "database.driver": "mongodb",  
    # "database.database": "datakline",
    # "database.host": "localhost",
    # "database.port": 27017,
    # "database.user": "",
    # "database.password": "",
    # "database.authentication_source": "admin"
}


# Load global setting from json file.
SETTING_FILENAME: str = "vt_setting.json"
SETTINGS.update(load_json(SETTING_FILENAME))
