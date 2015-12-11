#!/usr/bin/python3

import argparse
import json
import stopInfo
from argparse import ArgumentParser, RawTextHelpFormatter

parser = ArgumentParser(description='Find out how close the next bus is.', formatter_class=RawTextHelpFormatter)
parser.add_argument('api_key', type=str, help='MTA Bustime API key')
parser.add_argument('bus_line', type=str, help='Bus line in the form Q35, B44-SBS, etc.')
parser.add_argument('stop_id', type=str, help='GTFS stop ID of the stop you want to monitor. Ex: 309214')
parser.add_argument('format', type=str, help='Format for printing out the data. Supports following substitutions:\n    %%l - the line\n    %%r - the route\n    %%s - # of stops away\n    %%H - # of hours away\n    %%M - # of minutes away\n    %%S - # of seconds away\n    %%T - deltatime-native time output')
args = parser.parse_args()

bus = stopInfo.stopInfo(args.api_key,args.bus_line,args.stop_id)
bus.printf(args.format)
