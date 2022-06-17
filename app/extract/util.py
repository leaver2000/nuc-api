from typing import overload
from datetime import datetime, timedelta

@overload
def tomorrow(hour:int=None, minute:int=None, second:int=None) ->datetime:...
def tomorrow(**kwargs):
    tomorrow = datetime.utcnow() + timedelta(days=0)
    return datetime(**{xx: getattr(tomorrow, xx ) for xx in ("year", "month","day") }|kwargs)