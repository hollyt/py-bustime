#!/usr/bin/python3

import argparse
from datetime import datetime, timedelta, timezone
import requests
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
    def __init__(self, api_key, bus_line, stop_id, direction):
        self.api_key = api_key
        self.bus_line = 'MTA NYCT_{}'.format(bus_line)
        self.stop_id = stop_id
        self.direction = direction
        self.last_updated = None
        # TODO: remove hardcoded timezone
        self.local_tz = timezone(timedelta(hours=-5))
        self.update()

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
            response = requests.get(STOP_URL, params=request).json()
            response_time_local = datetime.now(tz=self.local_tz)
        except:
            print('Error making HTTP request.')
            exit(1)
        stop_time = response['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]
        self.response_time = parse_datetime(stop_time['ResponseTimestamp'])
        self.valid_till = parse_datetime(stop_time['ValidUntil'])
        self.clock_skew = self.response_time - response_time_local
        stopvisits = response['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
        self.buses = [Bus(bus) for bus in stopvisits]

    def outdated(self):
        rightnow = datetime.now(tz=self.local_tz)
        return (self.response_time == None or
            self.valid_till <= rightnow+self.clock_skew)

    def printf(self, fmt):
        if self.outdated():
            self.update()
        for bus in self.buses:
            now = datetime.now(tz=self.local_tz)+self.clock_skew
            print(bus.printf(fmt,now))

class Bus:
    def __init__(self,info):
        journey = info['MonitoredVehicleJourney']
        monitoredCall = journey['MonitoredCall']
        try:
            self.arrival_time = parse_datetime(monitoredCall['ExpectedArrivalTime'])
        except KeyError:
            self.arrival_time = None
        self.line = journey['PublishedLineName']
        self.route = journey['DestinationName']
        distances = monitoredCall['Extensions']['Distances']
        self.stops_away = distances['StopsFromCall']

    def printf(self, fmt, now=None):
        time_till = self.arrival_time-now if now is not None else None
        time_till = time_till - timedelta(microseconds=time_till.microseconds) if now is not None else None # truncate microseconds for printing
        hours_till = str(time_till.seconds//3600).zfill(2) if now is not None else None
        minutes_till = str((time_till.seconds//60)%60).zfill(2) if now is not None else None
        seconds_till = str(time_till.seconds%60).zfill(2) if now is not None else None
        fmt_table = {'%l': self.line,
                     '%r': self.route,
                     '%s': self.stops_away,
                     '%H': hours_till,
                     '%M': minutes_till,
                     '%S': seconds_till,
                     '%T': str(time_till)}
        for key in fmt_table:
            fmt = fmt.replace(key,str(fmt_table[key]))
        return fmt

def main():
    parser = argparse.ArgumentParser(description='Find out how close the next bus is.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('api_key', type=str, help='MTA Bustime API key')
    parser.add_argument('bus_line', type=str, help='Bus line in the form Q35, B44-SBS, etc.')
    parser.add_argument('stop_id', type=int, help='GTFS stop ID of the stop you want to monitor. Ex: 309214')
    parser.add_argument('-d', '--direction', choices=[0,1], default=None, help='Some stops are not unique in terms of bus direction. In this case,\nyou can enter 0 or 1 to specify direction. Default is to show both.')
    parser.add_argument('-f', '--format', type=str, default='%l [%r]\t%s stops away\t%M minutes away',help='Format for printing out the data. Supports following substitutions:\n    %%l - the line\n    %%r - the route\n    %%s - # of stops away\n    %%H - # of hours away\n    %%M - # of minutes away\n    %%S - # of seconds away\n    %%T - deltatime-native time output')
    args = parser.parse_args()

    stop = stopInfo(args.api_key,args.bus_line,args.stop_id,args.direction)
    stop.printf(args.format)

if __name__ == '__main__':
    main()
