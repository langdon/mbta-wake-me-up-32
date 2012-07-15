import urllib
import json
from bottle import route, run, HTTPError, debug, template, static_file

#debug(True)

_LOCAL_DATA_URL = 'http://localhost:8090/Data/{0}'
_LOCAL_STATION_DATA_URL = 'http://localhost:8090/stations'
_CODE_FULL_PATH = '/home/lwhite/Documents/aptana-python32-scl/mbta-wake-me-up-32/src'

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
        row["StationName"] = _get_station_name(system, line, row["PlatformKey"])
    return line_data_obj

_system_info = {}

def _get_system_info(system):
    if (system not in _system_info):
        system_raw = urllib.request.urlopen(_LOCAL_STATION_DATA_URL)
        system_obj = json.loads(system_raw.read().decode('utf-8'))
        system_info_dict = {}
        for row in system_obj:
            if (row["Line"] not in system_info_dict):
                system_info_dict[row["Line"]] = {}
            system_info_dict[row["Line"]["PlatformKey"]] = row
            
        _system_info[system] = system_info_dict

    return _system_info[system]

def _get_platform_info(system, line, station):
    return _get_system_info(system)[line][station]

def _get_station_name(system, line, station):
    return _get_system_info(system)[line][station]["StationName"]

@route('/<system>/<line>/<station>/trains')
def get_nearby_trains(system, line, station):
    line_data_obj = _get_line_data(system, line)
     
    out_trains = []
    for row in line_data_obj:
        if (row["PlatformKey"] == station):
            out_trains.append(row) 
    return json.dumps(out_trains)

@route('/<system>/<line>/<trip>/<station>')
def get_next_stations(system, line, trip, station):
    line_data_obj = _get_line_data(system, line)
     
    out_stations = []
    for row in line_data_obj:
        #assumes predicted must be after current station, 
        #station still passed in case needed in the future
        if (row["Trip"] == trip) & (row["InformationType"] == "Predicted"): 
            out_stations.append(row)
    return json.dumps(out_stations)

#===============================================================================
# 
# 
# @route('/<route>/<train>/<stop>')
# @route('/<route>/<train>')
# @route('/<route>')
# def get_route_live_data(route):
#    #try:
#    route_data_raw = urllib.request.urlopen(_LOCAL_DATA_URL.format(route))
#    route_data_bin = route_data_raw.read()
#    route_data_arr = route_data_bin.split("\n")
#    
#    #except urllib.error.URLError, e:
#    #route_data_str = route_data.sp.decode("utf8").split("\n")
#    #print( route_data_str )
#    
#    route_data_parsed = csv.reader(route_data_arr.decode( "utf8"))
#    #route_data_parsed = csv.reader(route_data_bin.decode( "utf8"), newline="\n")
#    out = ""
#    for row in route_data_parsed:
#        if (len(row) >= 3):
#            out += row[3] + "\n"
#        else: 
#            out += "\n".join(row)
#    return out
# 
# @route('/<system>/<route>/<station>/trains')
# def get_nearby_trains(route):
#    #try:
#    route_data_raw = urllib.request.urlopen(_LOCAL_DATA_URL.format(route))
#    route_data_bin = route_data_raw.read()
#    route_data_arr = route_data_bin.split("\n")
#    
#    #except urllib.error.URLError, e:
#    #route_data_str = route_data.sp.decode("utf8").split("\n")
#    #print( route_data_str )
#    
#    route_data_parsed = csv.reader(route_data_arr.decode( "utf8"))
#    #route_data_parsed = csv.reader(route_data_bin.decode( "utf8"), newline="\n")
#    out = ""
#    for row in route_data_parsed:
#        if (len(row) >= 3):
#            out += row[3] + "\n"
#        else: 
#            out += "\n".join(row)
#    return out
# 
# def get_train_live_data(route):
#    lcase_route = route.lower
#    if (route == "red"):
#        csv.reader(open('{0}_log.txt'.format(lcase_route), newline=''), delimiter=',', quotechar='')
#===============================================================================

run(host='localhost', port=8080, reloader=True)
