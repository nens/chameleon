from gpiozero import Button, LED
from data import fetch_data, max_rain

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

NORTH_RED = LED("BOARD5")
NORTH_GREEN = LED("BOARD3")
EAST_RED = LED("BOARD19")
EAST_YELLOW = LED("BOARD21")
EAST_GREEN = LED("BOARD15")
SOUTH_RED = LED("BOARD11")
SOUTH_GREEN = LED("BOARD7")
WEST_RED = LED("BOARD13")
WEST_YELLOW = LED("BOARD29")
WEST_GREEN = LED("BOARD23")

NORTH_RED, NORTH_GREEN, EAST_RED, EAST_YELLOW, EAST_GREEN, SOUTH_RED, SOUTH_GREEN, WEST_RED, WEST_YELLOW, WEST_GREEN

ALL = [NORTH_RED, NORTH_GREEN, EAST_RED, EAST_YELLOW, EAST_GREEN, SOUTH_RED, SOUTH_GREEN, WEST_RED, WEST_YELLOW, WEST_GREEN]

REDS = [NORTH_RED, EAST_RED, SOUTH_RED, WEST_RED]
YELLOWS = [EAST_YELLOW, WEST_YELLOW]
GREENS = [NORTH_GREEN, EAST_GREEN, SOUTH_GREEN, WEST_GREEN]

NORTH = [NORTH_RED, NORTH_GREEN]
EAST = [EAST_RED, EAST_YELLOW, EAST_GREEN]
SOUTH = [SOUTH_RED, SOUTH_GREEN]
WEST = [WEST_RED, WEST_YELLOW, WEST_GREEN]

ON = Button("BOARD8")
OFF = Button("BOARD10")
MANUAL = Button("BOARD12")
AUTO = Button("BOARD16")
BUTTON = Button("BOARD18", bounce_time=500)

IN = [ON, OFF, MANUAL, AUTO, BUTTON]

BUTTON_PRESSED = False

MODE_OFF = 1
MODE_MANUAL = 2
MODE_STANDUP = 3
MODE_LUNCH = 4
MODE_STATUS = 5

def fetch_weather_data(timeframe=timeframe):
    temperature, windspeed, raindata = fetch_data(latitude=latitude, longitude=longitude, timeframe=timeframe)
    rain_peak = max_rain(rain_data=raindata, timeframe=timeframe) if raindata != None else None
    return temperature, windspeed, rain_peak


