from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from buienradar.buienradar import (get_data, parse_data)
from buienradar.constants import (CONTENT, RAINCONTENT, SUCCESS)

timezone = ZoneInfo("Europe/Amsterdam")


def string_to_datetime(timestamp):
    strhour, strminute = timestamp.split(":")
    hour = int(strhour)
    minute = int(strminute)
    five_minutes_ago = datetime.now(tz=timezone) - timedelta(minutes=5)
    now = datetime.now()
    timestamp = datetime(year=now.year, month=now.month, day=now.day, hour=hour, minute=minute, tzinfo=timezone)

    if timestamp < five_minutes_ago:
        timestamp += timedelta(days=1)
    
    return timestamp


def parse_rain_data(raindata):
    split_response = raindata.strip().split("\r\n")
    split_tuple_response = list(i.split("|") for i in split_response)
    return list({"timestamp": string_to_datetime(timestamp), "mmh": int(mmh)/100} for mmh, timestamp in split_tuple_response)

def fetch_data(latitude, longitude, timeframe):
    response = get_data(latitude=latitude,
                    longitude=longitude,
                    )

    if response.get(SUCCESS):
        data = response[CONTENT]
        raindata = response[RAINCONTENT]

        result = parse_data(data, raindata, latitude, longitude, timeframe)["data"]

        temperature = result["temperature"]
        windspeed = result["windspeed"]
        parsed_rain_data = parse_rain_data(raindata=raindata)
        return temperature, windspeed, parsed_rain_data
    else:
        return None, None, None


def max_rain(rain_data, timeframe):
    max_rain = 0

    now_plus_offset = datetime.now(tz=timezone) + timedelta(minutes=timeframe)
    for i in rain_data:
        if i["timestamp"] <= now_plus_offset:
            max_rain = max(max_rain, i["mmh"])
        else:
            break

    return max_rain
