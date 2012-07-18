import urllib
import json
from bottle import route, run, HTTPError, debug, template, static_file

#debug(True)
import sys
print ('current trace function', sys.gettrace())


_LOCAL_DATA_URL = 'http://localhost:8090/Data/{0}'
_LOCAL_STATION_DATA_URL = 'http://localhost:8090/stations'
_CODE_FULL_PATH = '/home/lwhite/Documents/aptana-python-wkspc/mbta-wake-me-up-32/src'

@route('/')
@route('/index')
@route('/index.html')
@route('/index.htm')
def index():
    return template('index')

@route('/css/<filepath:path>')
def server_css(filepath):
    return static_file(filepath, root= _CODE_FULL_PATH + '/css')

@route('/scripts/<filepath:path>')
def server_scripts(filepath):
    return static_file(filepath, root= _CODE_FULL_PATH + '/scripts')

def _get_line_data(system, line):
    line_data_raw = urllib.request.urlopen(_LOCAL_DATA_URL.format(line))
    line_data_obj = json.loads(line_data_raw.read().decode('utf-8'))
    for row in line_data_obj:
        row['StationName'] = _get_station_name(system, line, row['PlatformKey'])
    return line_data_obj

_system_info = {}

def _get_system_info(system):
    if (system not in _system_info):
        system_raw = urllib.request.urlopen(_LOCAL_STATION_DATA_URL)
        system_obj = json.loads(system_raw.read().decode('utf-8'))
        system_info_dict = {}
        for row in system_obj:
            row['Line'] = row['Line'].lower()
            if (row['Line'] not in system_info_dict):
                system_info_dict[row['Line']] = {}
            system_info_dict[row['Line']][row['PlatformKey']] = row
            
        _system_info[system] = system_info_dict
        #print(_system_info[system])

    return _system_info[system]

def _get_platform_info(system, line, station):
    return _get_system_info(system)[line][station]

def _get_station_name(system, line, station):
    return _get_system_info(system)[line][station]['StationName'].title()

@route('/<system>/<line>/<station>/trains')
def get_nearby_trains(system, line, station):
    line_data_obj = _get_line_data(system, line)
     
    out_trains = []
    for row in line_data_obj:
        if (row['PlatformKey'] == station):
            out_trains.append(row) 
    return json.dumps(out_trains)

@route('/<system>/<line>/<trip>/<station>')
def get_next_stations(system, line, trip, station):
    line_data_obj = _get_line_data(system, line)
     
    out_stations = []
    print("Received " + str(len(line_data_obj)) + " stations; testing for trip=" + trip + " and InformationType=Predicted")
    for row in line_data_obj:
        #assumes predicted must be after current station, 
        #station still passed in case needed in the future
        trip = int(trip)
        if (row['Trip'] == trip) and (row['InformationType'] == 'Predicted'): 
            print("Found row: " + str(row))
            out_stations.append(row)
    return json.dumps(out_stations)

run(host='localhost', port=8080, reloader=True)
