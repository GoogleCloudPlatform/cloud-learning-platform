"""Utility methods for caching related operations."""
import datetime
import json
import redis

r = redis.Redis(host="redis-master", port=6379, db=0)

def json_serial(obj):
  """JSON serializer for objects not serializable by default json code"""
  if isinstance(obj, (datetime.datetime, datetime.date,datetime.time)):
    return obj.isoformat()
  raise TypeError (f"Type {type(obj)} not serializable")

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
  value = json.dumps(value,default=json_serial)
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
