from functools import wraps
from json import dumps

def to_json(func):
  @wraps(func)
  def wrapped(*args, **kwargs):
    result = func(*args, **kwargs)
    return dumps(result)

  return wrapped
