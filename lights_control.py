from gpiozero import Button, LED
from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth


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

ALL = {
   "NORTH_RED": NORTH_RED,
   "NORTH_GREEN": NORTH_GREEN,
   "EAST_RED": EAST_RED,
   "EAST_YELLOW": EAST_YELLOW,
   "EAST_GREEN": EAST_GREEN,
   "SOUTH_RED": SOUTH_RED,
   "SOUTH_GREEN": SOUTH_GREEN,
   "WEST_RED": WEST_RED,
   "WEST_YELLOW": WEST_YELLOW,
   "WEST_GREEN": WEST_GREEN
}

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
BUTTON = Button("BOARD18", bounce_time=0.3)

IN = [ON, OFF, MANUAL, AUTO, BUTTON]

BUTTON_PRESSED = False

MODE_OFF = 1
MODE_MANUAL = 2
MODE_STANDUP = 3
MODE_LUNCH = 4
MODE_STATUS = 5


for led in ALL.values():
    led.off()



with open("TOKEN", "r") as f:
    API_TOKEN = f.read()

tokens = {
    API_TOKEN: "internal"
}

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@auth.error_handler
def auth_error(status):
    return jsonify({"status": status, "message": "Access denied"}), status

@app.route("/")
def main():
    # For each led, read the led state and store it in the leds dictionary:
    leds = dict((led, {'name': led, 'state': ALL[led].is_lit}) for led in ALL.keys())
    # Put the leds dictionary into the template data dictionary:
    template_data = {
        'leds' : leds
    }
    # Pass the template data into the template main.html and return it to the user
    return jsonify(template_data)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/set_state", methods=['POST'])
@auth.login_required
def action():
    input_json = request.get_json(force=True)
    if "pin" not in input_json.keys() or "state" not in input_json.keys():
        return jsonify({"status": 400, "message": f"You must specify a pin (choose from {ALL.keys()}) and a boolean state"}), 400
    change_pin = input_json["pin"]
    if change_pin not in ALL.keys():
        return jsonify({"status": 400, "message": f"{change_pin} is unavailable. Choose from {ALL.keys()}"}), 400
    state = input_json["state"]
    if state not in [True, False]:
        return jsonify({"status": 400, "message": f"{state} is not a valid state; use true or false"}), 400
    # Convert the pin from the URL into a LED variable:
    change_led = ALL[change_pin]
    if state == change_led.is_lit:
        return jsonify({"status": 200, "message": f"{change_pin} is already {state}; no changes applied"}), 200
    # If the action part of the URL is "on," execute the code indented below:
    if state == True:
        # Set the pin high:
        change_led.on()
        # Save the status message to be passed into the template:
    elif state == False:
        change_led.off()
    return "", 204


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)

