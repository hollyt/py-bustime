#!/usr/bin/python3

import argparse
import json
import stopInfo

parser = argparse.ArgumentParser(description='Find out how close the next bus is.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('api_key', type=str, help='MTA Bustime API key')
parser.add_argument('bus_line', type=str, help='Bus line in the form Q35, B44-SBS, etc.')
parser.add_argument('stop_id', type=int, help='GTFS stop ID of the stop you want to monitor. Ex: 309214')
parser.add_argument('-d', '--direction', choices=[0,1], default=None, help='Some stops are not unique in terms of bus direction. In this case,\nyou can enter 0 or 1 to specify direction. Default is to show both.')
parser.add_argument('-f', '--format', type=str, default='%l [%r]\t%s stops away\t%M minutes away',help='Format for printing out the data. Supports following substitutions:\n    %%l - the line\n    %%r - the route\n    %%s - # of stops away\n    %%H - # of hours away\n    %%M - # of minutes away\n    %%S - # of seconds away\n    %%T - deltatime-native time output')
args = parser.parse_args()

stop = stopInfo.stopInfo(args.api_key,args.bus_line,args.stop_id,args.direction)
stop.printf(args.format)
