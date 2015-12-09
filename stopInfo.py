#!/usr/bin/python3

import json
import requests
from datetime import datetime, timezone, timedelta
import time

# A python library for tracking MTA buses

STOP_URL = 'http://bustime.mta.info/api/siri/stop-monitoring.json'

def parse_datetime(s):
    date = s[0:10].split('-')
    time = s[11:19].split(':') # not interested in milliseconds
    tz = s[23:].split(':')
    return datetime(int(date[0]), int(date[1]), int(date[2]),
            hour=int(time[0]), minute=int(time[1]), second=int(time[2]),
            tzinfo=timezone(timedelta(hours=int(tz[0]),minutes=int(tz[1]))))

class stopInfo:
    def __init__(self, api_key, bus_line, stop_id):
        self.api_key = api_key
        self.bus_line = 'MTA NYCT_{}'.format(bus_line)
        self.stop_id = stop_id
        self.last_updated = None
        # TODO: remove hardcoded timezone
        self.local_tz = timezone(timedelta(hours=-5))
        self.update()

    def outdated(self):
        rightnow = datetime.now(tz=self.local_tz)
        return (self.response_time == None or
            self.valid_till <= rightnow+self.clock_skew)

    def update(self):
        request = {
            'key': self.api_key,
            'OperatorRef': 'MTA',
            'MonitoringRef': self.stop_id,
            'LineRef': self.bus_line,
            'DirectionRef': None,
            'MaximumStopVisits': 4
        }
        try:
            hugedump = requests.get(STOP_URL, params=request).json()
            response_time_local = datetime.now(tz=self.local_tz)
        except:
            print('Error making HTTP request.')
            exit(1)
        stopmon = hugedump['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]
        self.response_time = parse_datetime(stopmon['ResponseTimestamp'])
        self.valid_till = parse_datetime(stopmon['ValidUntil'])
        self.clock_skew = self.response_time - response_time_local
        stopvisits = hugedump['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
        self.buses = [Bus(bus) for bus in stopvisits]

    def print_data(self):
        if self.outdated():
            self.update()
        for bus in self.buses:
            print(bus.format_data())

class Bus:
    def __init__(self,info):
        journey = info['MonitoredVehicleJourney']
        monitoredCall = journey['MonitoredCall']

        self.arrival_time = parse_datetime(monitoredCall['ExpectedArrivalTime'])
        self.line = journey['PublishedLineName']
        self.route = journey['DestinationName']
        distances = monitoredCall['Extensions']['Distances']
        self.stops_away = distances['StopsFromCall']

    def format_data(self):
        return '{}[[{}]]: {} STOPS AWAY'.format(self.line,self.route,self.stops_away)

