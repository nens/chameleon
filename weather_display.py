from data_interface import fetch_data, max_rain


"""
All the factors are measured over a certain upcoming time period; an hour by default.

North shows whether it is blowing
Red > 7 m/s
Green > 1 m/s, < 7 m/s
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

# minutes to look ahead for precipitation forecast
# (5..120)
timeframe = 15

# gps-coordinates for the weather data
latitude = 52.09193
longitude = 5.1166653


def fetch_weather_data(timeframe=timeframe):
    temperature, windspeed, raindata = fetch_data(latitude=latitude, longitude=longitude, timeframe=timeframe)
    rain_peak = max_rain(rain_data=raindata, timeframe=timeframe) if raindata != None else None
    return temperature, windspeed, rain_peak
