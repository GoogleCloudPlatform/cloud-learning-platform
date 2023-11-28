"""Utility methods for caching related operations."""
import datetime
import json
import redis
from common.config import MEMORYSTORE_ENABLED
from common.utils.secrets import get_secret
from common.utils.logging_handler import Logger

if MEMORYSTORE_ENABLED == "true":
  host = get_secret("memorystore-master-host")
  host = host.split(":")
  host_ip = host[0]
  host_port = host[1]
  r = redis.Redis(host=host_ip, port=host_port, db=0)
else:
  r = redis.Redis(host="redis-master", port=6379, db=0)


def json_serial(obj):
  """JSON serializer for objects not serializable by default json code"""
  if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
    return obj.isoformat()
  raise TypeError(f"Type {type(obj)} not serializable")


def set_key(key, value, expiry_time=3600):
  """
        Stores value against key in cache with default expiry time of 1hr
        Args:
            key: String
            value: String or Dict or Number
            exp: Number(Expiry time in Secs, default 3600)
        Returns:
            True or False
    """
  value = json.dumps(value, default=json_serial)
  Logger.info(f"Set Key FUnction {MEMORYSTORE_ENABLED} {host}")
  return r.set(key, value, ex=expiry_time)


def get_key(key):
  """
        Checks for key in cache, if found then, Returns value against that key
        else Returns None
        Args:
            key: String
        Returns:
            value: String or Dict or Number or None
    """
  value = r.get(key)
  return_value = json.loads(value) if value is not None else None
  Logger.info(f"Get Key FUnction {MEMORYSTORE_ENABLED} {host}")
  return return_value


def delete_key(key):
  r.delete(key)


def set_key_normal(key, value, expiry_time=3600):
  """
        Stores value against key in cache with default expiry time of 1hr
        Args:
            key: String
            value: String or Dict or Number
            exp: Number(Expiry time in Secs, default 3600)
        Returns:
            True or False
    """
  return r.set(key, value, ex=expiry_time)


def get_key_normal(key):
  """
        Checks for key in cache, if found then, Returns value against that key
        else Returns None
        Args:
            key: String
        Returns:
            value: String or Dict or Number or None
    """

  return r.get(key)
