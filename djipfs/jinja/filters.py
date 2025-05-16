import ast
from datetime import datetime, timedelta, timezone

# init current time
current_timestamp = datetime.now(timezone.utc)

def dateformat(value):
    return f'{value.strftime("%B")} {value.strftime("%d")}, {value.strftime("%Y")}'
