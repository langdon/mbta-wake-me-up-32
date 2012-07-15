from bottle import route, run, HTTPError
import urllib # using full name because of conflict with bottle
import json


_DATA_FILE_PATH = '../data/{0}_log.json'
_MBTA_DATA_URL = 'http://developer.mbta.com/Data/{0}.json'

_PLATFORM_FILE_PATH = '../data/RealTimeHeavyRailKeys.csv'
_MBTA_PLATFORM_URL = 'http://developer.mbta.com/RT_Archive/RealTimeHeavyRailKeys.csv'


@route('/Data/<route>')
def line_info(route):
    # takes the route you want data for and will retrieve it from MBTA, 
    # if the connection fails it will default to some sample data
    if (route.lower() in ['red', 'blue', 'orange']):
        try:
            route_data = urllib.request.urlopen(
                _MBTA_DATA_URL.format(route.capitalize()), timeout=5
                )
            return route_data.read()
        except urllib.error.URLError: # includes HTTPError
            return _local_line_info(route)
    raise HTTPError()
    
def _local_line_info(route):
    # takes the route that you want data for, legal routes are 'red', 'orange', 
    # 'blue'. However, data only exists for 'red'.
    lcase_route = route.lower()
    if (lcase_route in ['red', 'blue', 'orange']):
        try:
            return open(_DATA_FILE_PATH.format(str(lcase_route)), mode='rb')
        except IOError:
            raise HTTPError(404, output="No data for given route")
    raise HTTPError()

@route('/stations')
def get_system_info():
    f = open(_PLATFORM_FILE_PATH,'r')
    
    arr=[]
    headers = []
    
    for header in f.readline().split(','):
        headers.append(header)
    
    for line in f.readlines():
        lineItems = {}
        for i,item in enumerate(line.split(',')):  
            lineItems[headers[i]] = item
        arr.append(lineItems)
    
    f.close()
    return json.dumps(arr)

run(host='localhost', port=8090)
