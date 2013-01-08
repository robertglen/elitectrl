#!/usr/local/bin/python
"""
Script to send the eight character ASCII codes to a Sharp Elite TV
to power on or off the unit.

This is one of my first python scripts so I doubt it is a good coding
example, but it works.

It can be expanded further to include many other TV functions which would
likely require massive expansion of the argument parsing so as to not assume
we want to work exclusively with power control.
"""

# Import standard modules
import sys
import socket
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description="Turn on or off your Sharp Elite LED TV")
parser.add_argument("host", help="IP address or hostname")
parser.add_argument("port", help="TCP port used for IP control", type=int)
parser.add_argument("power", help="Turn power on or off", choices=['on','off'])
args = parser.parse_args()

# Define the function sending the ASCII message
def sendCmd(cmd):
  try:
    eliteIP = socket.gethostbyname(args.host)
    # Comment here for git
  except socket.gaierror:
    sys.stderr.write('DNS failure: cannot resolve ' + args.host + '\n')
    sys.exit(1)

  try:
    # Create a socket object
    s = socket.socket()
    # Define a socket timeout before making a connection
    s.settimeout(1.0)
    # Connect the socket to the elite 
    s.connect((eliteIP,args.port))
    # Send the Sharp/Elite 8 character ASCII code to power off
    s.send(cmd)
  except socket.timeout:
    sys.stderr.write('socket timed out while connecting to ' + args.host + ':' + str(args.port) + '\n')
    sys.stderr.write('Make sure the TV is configured to allow IP control and the IP:port is correct\n')
    if args.power == 'on':
      sys.stderr.write('Finally, make sure the power off mode is set to standby (not the default off mode)\n')
  except socket.error:
    sys.stderr.write('Could not connect to ' + args.host + ':' + str(args.port) + '\n')
    sys.stderr.write('Make sure the TV is configured to allow IP control and the IP:port is correct\n')
  finally:
    # Close the socket connection regardless
    s.close()

def main():
  # Convert the simple on/off into Elite ASCII commands
  if args.power == 'on': 
    cmd = 'POWR1   \r'
  else:
    cmd = 'POWR0   \r'

  # Call the sendCmd function with the cmd
  sendCmd(cmd)

# Call main function
if __name__ == '__main__':
  main()

