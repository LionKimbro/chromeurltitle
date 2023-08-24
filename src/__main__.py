"""run.py  -- chassis2023 TCPSERVER run command for bookmarkreceiver"""

import chassis2023


# Chassis 2023 will detect that this program is a
# WEBSERVER, start a server process from configuration paramaters,
#
# The first time this program runs, the session configuration will be
# created, and the program will abort with information about how to
# perform configuration.
#
#
# Command line parameters can be used to specify the configuration information,
# and to bypass the 1st-time configuration halt.
#
# It needs a host (defaults to ""), and it needs a port to host on.
# This is, by default.
#
#
# After it is verified that all the information required is present,
# chassis2023 will 
chassis.run()

