#!/usr/bin/python

import json
import requests

# A python library for tracking MTA buses

STOP_URL = 'http://bustime.mta.info/api/siri/stop-monitoring.json'

class stopInfo:
    def __init__(self, api_key, bus_line, stop_id):
        self.api_key = api_key
        self.bus_line = 'MTA NYCT_{}'.format(bus_line)
        self.stop_id = stop_id
        self.busstop_data = self.create_request()
        self.parsed_data = self.parse_request()

    def create_request(self):
        request = {
            'key': self.api_key,
            'OperatorRef': 'MTA',
            'MonitoringRef': self.stop_id,
            'LineRef': self.bus_line,
            'DirectionRef': None,
            'MaximumStopVisits': 4
        }
        try:
            busstop_data = requests.get(STOP_URL, params=request).json()
        except:
            print('Error making HTTP request.')
            exit(1)
        return busstop_data

    # A LOT of extra info gets sent in the response. For now I'm only keeping
    # what I want to display.
    def parse_request(self):
        unpack_JSON = self.busstop_data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
        approaching_busses = [Bus(bus) for bus in unpack_JSON]
        return approaching_busses

    def print_data(self):
        for bus in self.parsed_data:
            print(bus.format_data())

class Bus:
    def __init__(self,info):
        # TODO: parse the arrival time
        journey = info['MonitoredVehicleJourney']
        monitoredCall = journey['MonitoredCall']

        self.arrival_time = monitoredCall['ExpectedArrivalTime']
        self.line = journey['PublishedLineName']
        self.route = journey['DestinationName']
        distances = monitoredCall['Extensions']['Distances']
        self.stops_away = distances['StopsFromCall']

    def format_data(self):
        return '{}[[{}]]: {} STOPS AWAY'.format(self.line,self.route,self.stops_away)

