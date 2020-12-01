import pytz
from datetime import datetime, timedelta


sa_timezone = pytz.timezone('America/Sao_Paulo')
utc_timezone = pytz.utc


def current_zoned_datetime(zone):
    timezone = pytz.timezone(zone)
    return timezone.localize(datetime.now())


def current_zoned_datetime_with_range(zone, range_days=7):
    timezone = pytz.timezone(zone)
    current_datetime = datetime.now(timezone)
    days = round(range_days/2)
    return current_datetime - timedelta(days=days), current_datetime + timedelta(days=days)


def parse(datetime_str, fmt):
    return datetime.strptime(datetime_str, fmt)


def fix_timezone(datetime_value):
    given_datetime = datetime_value
    if datetime_value.tzinfo is None:
        given_datetime = utc_timezone.localize(datetime_value)
    return utc_timezone.normalize(given_datetime).astimezone(sa_timezone)
