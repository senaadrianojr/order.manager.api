import pytz
from datetime import datetime, timedelta
import re


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


def parse_with_fixed_tz(datetime_tz_str, fmt):
    str_tz = re.split(r'^\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}', datetime_tz_str)[1]
    str_datetime = datetime_tz_str.replace(str_tz, '')
    str_tz = str_tz.replace(':', '')
    fixed_datetime_tz = '{}{}'.format(str_datetime, str_tz)
    return datetime.strptime(fixed_datetime_tz, fmt).astimezone(utc_timezone)


def fix_timezone(datetime_value):
    given_datetime = datetime_value
    if datetime_value.tzinfo is None:
        given_datetime = utc_timezone.localize(datetime_value)
    return utc_timezone.normalize(given_datetime).astimezone(sa_timezone)
