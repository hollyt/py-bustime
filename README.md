# py-bustime
Python script & library for the MTA bustime api so you can catch your bus from the command line!

# dependencies:
+ `python3`
+ `requests module`
+ `[bustime developer API key](http://bustime.mta.info/wiki/Developers/Index)`

# usage ideas:

## plain old execution:
`./stopInfo.py [-h] [-d {0,1}] [-f FORMAT] api_key bus_line stop_id`

## put into conky for constant stop monitoring:
`${execi 40 /path/to/py-bustime/stopInfo.py <your args>}`
note that you can specify the format, so if you want your conky to display just
the "BUS: HH:MM away" or like, you can use `-f "%l: %H:%M away` option.
