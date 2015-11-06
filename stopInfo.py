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
		self.requests = self.create_request()

	def create_request(self):
		request = {
			'key': self.api_key,
			'OperatorRef': 'MTA',
			'MonitoringRef': self.stop_id,
			'LineRef': self.bus_line,
			'DirectionRef': None,
			'MaximumStopVisits': 4
		}
		response = requests.get(STOP_URL, params=request)
		return response

