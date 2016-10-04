# -*- coding: utf-8 -*-
# (c) Nelen & Schuurmans, see LICENSE.rst.

import RPi.GPIO as GPIO
import base64
import json
import random
import time
import urllib2

from datetime import datetime
from threading import Thread


BASE_URL = 'https://jenkins.lizard.net/job/nens/job'
USERNAME = 'sa_stoplicht_jenk'
PASSWORD = 'A9TXRfzy6QwoZnGrMFI2'

STATUS = 'none'

ALIVE = True

NORTH_RED = 5
NORTH_GREEN = 3
EAST_RED = 19
EAST_ORANGE = 21
EAST_GREEN = 15
SOUTH_RED = 11
SOUTH_GREEN = 7
WEST_RED = 13
WEST_ORANGE = 29
WEST_GREEN = 23

ALL = [3, 5, 7, 11, 13, 15, 19, 21, 23, 29]

REDS = [5, 19, 11, 13]
ORANGES = [21, 29]
GREENS = [3, 15, 7, 23]

NORTH = [5, 3]
EAST = [19, 21, 15]
SOUTH = [11, 7]
WEST = [13, 29, 23]

NONE = []

NEIGHBOURS = {
    NORTH_RED : [NORTH_GREEN, EAST_RED, EAST_ORANGE],
    NORTH_GREEN : [NORTH_RED, EAST_GREEN, EAST_ORANGE],
    EAST_RED : [EAST_ORANGE, NORTH_RED],
    EAST_ORANGE : [EAST_RED, EAST_GREEN] + NORTH,
    EAST_GREEN : [EAST_ORANGE, NORTH_GREEN]
}

ACROSS = {
    NORTH_RED : 11,
    NORTH_GREEN : 7,
    EAST_RED : 13,
    EAST_ORANGE : 29,
    EAST_GREEN : 23
}

ON = 8
OFF = 10
MANUAL = 12 
AUTO = 16
BUTTON = 18

IN = [ON, OFF, MANUAL, AUTO, BUTTON]

BUTTON_PRESSED = False

MODE_OFF = 1
MODE_MANUAL = 2
MODE_STANDUP = 3
MODE_LUNCH = 4
MODE_STATUS = 5

MORSE = {
  'a':'.-',
  'b':'-...',
  'c':'-.-.',
  'd':'-..',
  'e':'.',
  'f':'..-.',
  'g':'--.',
  'h':'....',
  'i':'..',
  'j':'.---',
  'k':'-.-',
  'l':'.-..',
  'm':'--',
  'n':'-.',
  'o':'---',
  'p':'.--.',
  'q':'--.-',
  'r':'.-.',
  's':'...',
  't':'-',
  'u':'..-',
  'v':'...-',
  'w':'.--',
  'x':'-..-',
  'y':'-.--',
  'z':'--..',
}

def getjenkins(uri):
    req = urllib2.Request("{}/{}".format(BASE_URL, uri))
    base64string = base64.b64encode('{}:{}'.format(USERNAME, PASSWORD))
    req.add_header("Authorization", "Basic {}".format(base64string))
    f = urllib2.urlopen(req)
    r = f.read()
    return json.loads(r)

def fetchstatus():
    global STATUS
    while ALIVE:
        jobs = ["hydra-core", "lizard-client", "lizard-nxt", "threedi"]
        response = []
        for job in jobs:
            res = getjenkins("{}/api/json?pretty=true".format(job))
            for branch in res["jobs"]:
                if branch["name"] == "master" or branch["name"].startswith("fixes"):
                    uri = "{}/job/{}/lastBuild/api/json?pretty=true".format(job, branch["name"])
                    res = getjenkins(uri)
                    response.append(res["result"])
                    if res["building"]:
                        response.append("BUILDING")
        new = 'none'
        for str, status in [('Failure', 'broken'), ('Aborted', 'broken'), ('Building', 'building'), ('Unstable', 'unstable'), ('Disabled', 'unstable'), ('Success', 'stable')]:
            if str.upper() in response:
                new = status
                break
        STATUS = new
        time.sleep(15)

def setup():
  GPIO.setmode(GPIO.BOARD)
  for pin in ALL:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
  for pin in IN:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=pressed, bouncetime=500)

def setall(on):
  if not get(ON):
    on = NONE
  for pin in ALL:
    GPIO.output(pin, pin in on)

def get(pin):
  return True if GPIO.input(pin) == 0 else False

def pressed(channel):
  global BUTTON_PRESSED
  BUTTON_PRESSED = True

def getmode():
  if not get(ON):
    return MODE_OFF
  if get(MANUAL):
    return MODE_MANUAL
  now = datetime.now()
  if now.weekday() > 4:
    return MODE_OFF
  if now.hour < 7 or now.hour > 17:
    return MODE_OFF
  if now.hour == 12 and now.minute > 14 and now.minute < 30:
    return MODE_STANDUP
  if now.hour == 12 and now.minute > 29:
    return MODE_LUNCH
  return MODE_STATUS

def loop(t, lists, mode):
  while getmode() == mode:
    walk(t, lists)

def walk(t, lists):
  for lights in lists:
    setall(lights)
    time.sleep(t)

def dance(mode):
  prev_last = EAST_GREEN
  last = EAST_ORANGE
  i = 0
  while getmode() == mode and STATUS == 'building':
    n = list(NEIGHBOURS[last])
    n.remove(prev_last)
    r = int(random.random() * len(n))
    setall([last, ACROSS[last], n[r], ACROSS[n[r]]])
    time.sleep(0.08)
    setall([n[r], ACROSS[n[r]]])
    time.sleep(0.08)
    prev_last = last
    last = n[r]
    i += 1

def traffic(mode):
  global BUTTON_PRESSED
  if getmode() != mode:
    return
  setall([NORTH_RED, EAST_GREEN, SOUTH_RED, WEST_GREEN])
  while getmode() == mode and not BUTTON_PRESSED:
    time.sleep(0.1)
  BUTTON_PRESSED = False
  time.sleep(1)
  if getmode() != mode:
    return
  setall([NORTH_RED, EAST_ORANGE, SOUTH_RED, WEST_ORANGE])
  time.sleep(2)
  if getmode() != mode:
    return
  setall(REDS)
  time.sleep(1)
  if getmode() != mode:
    return
  setall([NORTH_GREEN, EAST_RED, SOUTH_GREEN, WEST_RED])
  while getmode() == mode and not BUTTON_PRESSED:
    time.sleep(0.1)
  BUTTON_PRESSED = False
  time.sleep(1)
  if getmode() != mode:
    return
  for i in range(0, 5):
    walk(0.2, [[EAST_RED, WEST_RED], [NORTH_GREEN, EAST_RED, SOUTH_GREEN, WEST_RED]])
  if getmode() != mode:
    return
  setall(REDS)
  time.sleep(1)

def morse(unit, msg, lights, mode):
  if getmode() == mode:
    for char in msg:
      if char == ' ':
        walk(unit * 7, [NONE])
        continue
      for code in MORSE[char]:
        if code == '.':
          walk(unit, [lights])
        if code == '-':
          walk(unit * 3, [lights])
        walk(unit, [NONE])
      walk(unit * 2, [NONE])
    walk(unit * 11, [NONE])

def available():
  now = datetime.now()
  return now.hour < 17

def dontwalk(lights):
  return intersect(lights, NORTH + EAST + WEST) + [SOUTH_RED]

def intersect(a, b):
  return list(set(a) & set(b))

def status(mode):
  while getmode() == mode:
    if STATUS == 'building':
      dance(mode)
      setall(NONE)
    elif STATUS == 'stable':
      setall(GREENS if available() else dontwalk(GREENS))
    elif STATUS == 'unstable':
      setall(ORANGES if available() else dontwalk(ORANGES))
    elif STATUS == 'none':
      HELP = [SOUTH_RED, WEST_ORANGE]
      FLASH = HELP + NORTH + EAST
      walk(0.02, [FLASH, HELP, HELP, HELP, FLASH, HELP])
    else:
      setall(REDS)
    time.sleep(1)

setup()
t = Thread(target=fetchstatus)
t.start()

try:
  while True:
    loop(0.37, [NONE], MODE_OFF)
    traffic(MODE_MANUAL)
    loop(0.74, [NONE, ORANGES], MODE_STANDUP)
    morse(0.125, 'carsten ga nou eens eten', ORANGES, MODE_LUNCH)
    status(MODE_STATUS)
except KeyboardInterrupt:
  GPIO.cleanup()
  ALIVE = False
  print (" - Killed! Waiting for the kid to die...")
except Exception as e:
  GPIO.cleanup()
  ALIVE = False
  raise e
