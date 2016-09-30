Chameleon
=========

This script monitors Lizard NXT build status and controls the traffic light.
Of courese there's also some monkey dancing going on in here.

WARNING! Pins 8, 10, 12, 16, 18 are physically wired to switches. NEVER set
those pins to 'OUT' mode as it will short circuit the pin to ground, potentially
burning the GPIO or the entire RasPi!

Setup
-----

git clone https://github.com/nens/chameleon.git

sudo python chameleon.py &


What does it mean?
------------------

Lights dictionary, Jenkins mode:

+-----------------------+-----------------------------------------------------------------+
| PERLIN NOISE          | Building...                                                     |
+-----------------------+-----------------------------------------------------------------+
| ALL GREEN             | All builds successfull                                          |
+-----------------------+-----------------------------------------------------------------+
| ALL ORANGE            | At least one build is unstable                                  |
+-----------------------+-----------------------------------------------------------------+
| ALL RED               | At least one build failed                                       |
+-----------------------+-----------------------------------------------------------------+
| MAIN GREEN, WALK RED  | All builds successfull, but do not walk in asking questions     |
+-----------------------+-----------------------------------------------------------------+
| MAIN ORANGE, WALK RED | At least one build is unstable, do not walk in asking questions |
+-----------------------+-----------------------------------------------------------------+
| ORANGE FLASHING       | Get up, stand up                                                |
+-----------------------+-----------------------------------------------------------------+
| ORANGE GOING BANANAS  | The light is trying to tell you something...                    |
+-----------------------+-----------------------------------------------------------------+
| ALL BLINKING TWICE    | Jenkins unreachable, could not determine build status           |
+-----------------------+-----------------------------------------------------------------+
| ALL OFF               | Out of office, go home                                          |
+-----------------------+-----------------------------------------------------------------+

Lights dictionary, traffic mode:

+-----------------------+-----------------------------------------------+
| MAIN GREEN, WALK RED  | Drive, don't walk; push the button to cross   |
+-----------------------+-----------------------------------------------+
| MAIN RED, WALK GREEN  | Walk, don't drive; push the button when tired |
+-----------------------+-----------------------------------------------+
| ALL OFF               | Out of office, go home                        |
+-----------------------+-----------------------------------------------+
