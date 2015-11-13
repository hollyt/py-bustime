#!/usr/bin/python

import argparse
import json
import stopInfo

parser = argparse.ArgumentParser(description='Find out how close the next bus is.')
parser.add_argument('api_key', type=str, help='MTA Bustime API key')
parser.add_argument('bus_line', type=str, help='Bus line in the form Q35, B44-SBS, etc.')
parser.add_argument('stop_id', type=str, help='GTFS stop ID of the stop you want to monitor. Ex: 309214')
args = parser.parse_args()

bus = stopInfo.stopInfo(args.api_key,args.bus_line,args.stop_id)
bus.print_data()
