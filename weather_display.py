from data_interface import fetch_data, max_rain
import requests
from pathlib import Path

"""
All the factors are measured over a certain upcoming time period; an hour by default.

North shows whether it is blowing
Red >= 7 m/s
Green >= 1 m/s, < 7 m/s
Off = < 1 m/s

East shows how much rain will fall at the highest peak
Red >= 5 mm/h
Orange < 5 mm/h, >= 2 mm/h
Green < 2 mm/h, > 0 mm/h
Off = 0 mm/h

West shows how cold it is
Green >= 20C
Orange < 20C, >= 10C
Red < 10C
"""

API_URL = "http://localhost:5000/"

NORTH = ["NORTH_RED", "NORTH_GREEN"]
EAST = ["EAST_RED", "EAST_YELLOW", "EAST_GREEN"]
WEST = ["WEST_RED", "WEST_YELLOW", "WEST_GREEN"]
ALL = [*NORTH, *EAST, *WEST]

# minutes to look ahead for precipitation forecast
# (5..120)
timeframe = 60

# gps-coordinates for the weather data
latitude = 52.09193
longitude = 5.1166653


def fetch_weather_data(timeframe=timeframe):
    temperature, windspeed, raindata = fetch_data(latitude=latitude, longitude=longitude, timeframe=timeframe)
    rain_peak = max_rain(rain_data=raindata, timeframe=timeframe) if raindata != None else None
    return temperature, windspeed, rain_peak


def wind_lights(wind: int) -> dict:
    wind_light_states = dict.fromkeys(NORTH, False)
    if wind >= 7:
        wind_light_states["NORTH_RED"] = True
    elif 1 <= wind < 7:
        wind_light_states["NORTH_GREEN"] = True
    return wind_light_states


def rain_lights(rain: int) -> dict:
    rain_light_states = dict.fromkeys(EAST, False)
    if rain >= 5:
        rain_light_states["EAST_RED"] = True
    elif 2 <= rain < 5:
        rain_light_states["EAST_ORANGE"] = True
    elif 0 < rain < 2:
        rain_light_states["EAST_GREEN"] = True
    return rain_light_states


def temperature_lights(temperature: int) -> dict:
    temperature_light_states = dict.fromkeys(WEST, False)
    if temperature >= 20:
        temperature_light_states["WEST_GREEN"] = True
    elif 10 <= temperature < 20:
        temperature_light_states["WEST_ORANGE"] = True
    elif temperature < 10:
        temperature_light_states["WEST_RED"] = True
    return temperature_light_states


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

p = Path(__file__).with_name("TOKEN")
with p.open("r") as f:
    API_TOKEN = f.read()

api_auth = BearerAuth(token=API_TOKEN)

def apply_light_states(light_states: dict) -> None:
    session = requests.Session()
    session.auth = api_auth
    for pin, state in light_states.items():
        session.post(
            url=f"{API_URL}set_state",
            json={
                "pin": pin,
                "state": state
            }
        )


def main():
    temperature, windspeed, rain_peak = fetch_weather_data()
    if all(value is None for value in (temperature, windspeed, rain_peak)):
        desired_light_states = dict.fromkeys(ALL, False)

    else:
        wind_light_states = wind_lights(wind=windspeed)
        rain_light_states = rain_lights(rain=rain_peak)
        temperature_light_states = temperature_lights(temperature=temperature)
        desired_light_states = {**wind_light_states, **rain_light_states, **temperature_light_states}        

    apply_light_states(light_states=desired_light_states)


if __name__ == "__main__":
    main()
