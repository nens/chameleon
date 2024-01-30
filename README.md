Chameleon
=========

This script monitors the weather at Nelen&Schuurmans (Vinkenburgstraat 2A) and controls the traffic light via a Flask API.

WARNING! Pins 8, 10, 12, 16, 18 are physically wired to switches. NEVER set
those pins to 'OUT' mode as it will short circuit the pin to ground, potentially
burning the GPIO or the entire RasPi!

Setup
-----

```bash
git clone https://github.com/nens/chameleon.git
python3 lights_control.py  # make this a service permanently running
python3 weather_display.py  # run this every few minutes from a cronjob
```


What does it mean?
------------------

All the factors are measured over a certain upcoming time period; an hour by default.


North shows whether it is blowing
```
Red >= 7 m/s
Green >= 1 m/s, < 7 m/s
Off = < 1 m/s
```

East shows how much rain will fall at the highest peak
```
Red >= 5 mm/h
Orange < 5 mm/h, >= 2 mm/h
Green < 2 mm/h, > 0 mm/h
Off = 0 mm/h
```

West shows how cold it is
```
Green >= 20C
Orange < 20C, >= 10C
Red < 10C
```
