"""
This program retrieve and return weather data based on given location information and type of weather information
requested through the uses of arguments
"""
import argparse
import sys
import requests
import datetime

# api key = '241662d8c926c731d81cddf5e783f8d8'

parser_global = None


def argument_parse(args):
    """
    This function takes in a list of arguments from sys.argv and process into the parser namespace.
    Invalid argument will directly stop the program and show which argument is invalid
    :param args: a list of arguments inputted at command line or manually using list
    :return: an parser object containing the namespace with data regarding arguments.
    """
    global parser_global
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("-help", help="show how to use the program", action='store_true')
    parser.add_argument("-api", metavar="= API token", help="Enter a API key to call the weather program")
    parser.add_argument("-city", metavar="= City name", help="Enter the name of a city")
    parser.add_argument("-cid", metavar="= City ID", help="Enter a city's ID")
    parser.add_argument("-gc", metavar="= Geographic coordinates", help="Enter coordinates of a city (lat,lng)")
    parser.add_argument("-z", metavar="= zip code", help="Enter a city's zip code (z,country) or (z)")
    parser.add_argument("-time", help="Request to see time", action='store_true')
    parser.add_argument("-temp", nargs='?', const='celsius', metavar="= celsius/fahrenheit",
                        help="Request temperature (Specify celsius or fahrenheit)")
    parser.add_argument("-pressure", help="Request to see pressure", action='store_true')
    parser.add_argument("-cloud", help="Request to see cloud status", action='store_true')
    parser.add_argument("-humidity", help="Request to see humidity", action='store_true')
    parser.add_argument("-wind", help="Request to see wind speed and degree", action='store_true')
    parser.add_argument("-sunset", help="Request to see sunset data", action='store_true')
    parser.add_argument("-sunrise", help="Request to see sunrise data", action='store_true')

    parser_global = parser

    return parser.parse_args(args)


def request_help():
    """
    This function display help message using the parser's own in built print_help()
    :return: Boolean "True" if it executed print_help without issue.
    """
    parser_global.print_help()
    return True


def check_api_key(api_key):
    """
    This function check if the api key provided is valid
    :param api_key: a string value representing api key
    :return: True if data received properly, False along with error message otherwise.
    """
    request = requests.get(
        "http://api.openweathermap.org/data/2.5/forecast?q=London" + "&APPID=" + str(api_key) + "&units=metric")

    request_result = request.json()

    # cod == 200 indicate successful data retrieval
    if request_result['cod'] == '200':
        return [True, ""]
    else:
        return [False, "API key error: " + request_result['message']]


def check_for_location(args):
    """
    This function check for infeasible case of locations arguments.
    :param args: Arguments list stored in parser namespace
    :return: True if condition is correct, False if infeasible case detected
    """
    location_array = []
    location_counter = 0

    location_array.append(args.city)
    location_array.append(args.cid)
    location_array.append(args.gc)
    location_array.append(args.z)

    for i in location_array:
        if i is None:
            location_counter += 1

    if location_counter == 3:
        return [True, ""]
    elif location_counter == 4:
        return [False, "No location specified"]
    else:
        return [False, "Multiple chosen locations are specified"]


def request_by_city(api_key, city):
    """
    This function retrieve weather data using city name
    :param api_key: a string value representing api key
    :param city: a string representing the city name
    :return: the weather data result, if data retrieval failed, return None
    """

    request = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=" + str(city) + "&APPID=" + str(api_key) + "&units=metric")

    request_result = request.json()

    # cod == 200 indicate successful data retrieval
    if request_result['cod'] == 200:
        return request_result
    else:
        print("Request -city error: " + request_result['message'])
        return None


def request_by_id(api_key, cid):
    """
    This function retrieve weather data using city id
    :param api_key: a string value representing api key
    :param cid: a string representing the city id
    :return: the weather data result, if data retrieval failed, return None
    """

    request = requests.get(
    "http://api.openweathermap.org/data/2.5/weather?id=" + str(cid) + "&APPID=" + str(api_key) + "&units=metric")

    request_result = request.json()

    # cod == 200 indicate successful data retrieval
    if request_result['cod'] == 200:
        return request_result
    else:
        print("Request city ID -cid error: " + request_result['message'])
        return None


def request_by_gc(api_key, gc):
    """
    This function retrieve weather data using city coordinate
    :param api_key: a string value representing api key
    :param gc: a string representing the city coordinate
    :return: the weather data result, if data retrieval failed, return None
    """

    coordinates = gc.split(",")
    lat = coordinates[0]
    lng = coordinates[1]

    request = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lng) + "&APPID=" + str(api_key) + "&units=metric")

    request_result = request.json()

    # cod == 200 indicate successful data retrieval
    if request_result['cod'] == 200:
        return request_result
    else:
        print("Request coordinates -gc error: " + request_result['message'])
        return None


def request_by_z(api_key, z):
    """
    This function retrieve weather data using zip code
    :param api_key: a string value representing api key
    :param z: a string representing the zip code
    :return: the weather data result, if data retrieval failed, return None
    """

    request = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?zip=" + str(z) + "&APPID=" + str(api_key) + "&units=metric")

    if request is not None:
        request_result = request.json()
        # cod == 200 indicate successful data retrieval
        if request_result['cod'] == 200:
            return request_result
        else:
            print("Request zip code -z error: " + request_result['message'])
            return None


def request_temperature(result_response, temp_unit):
    """
    This function return temperature data using provided weather data and unit requested.
    Default unit is celsius.
    :param result_response: The weather data
    :param temp_unit: unit of temperature to display
    :return: False if temperature data retrieval error, else the temperature data
    """
    try:
        temp_min_celsius = result_response['main']['temp_min']
        temp_max_celsius = result_response['main']['temp_max']
    except:
        return [False, "Error: Temperature retrieval error"]

    if temp_unit.lower() == 'celsius':
        print_str = "The temperature ranges from " + str(temp_min_celsius) + " C" + "-" + str(temp_max_celsius) + " C"
        return [True, print_str]

    elif temp_unit.lower() == 'fahrenheit':
        temp_min_fahrenheit = round(float((temp_min_celsius * 9/5) + 32), 2)
        temp_max_fahrenheit = round(float((temp_max_celsius * 9/5) + 32), 2)

        print_str = "The temperature ranges from " + str(temp_min_fahrenheit) + " F" + "-" + str(temp_max_fahrenheit) + " F"
        return [True, print_str]

    else:
        print_str = "Invalid temperature format entered: temperature unable to display"
        return [False, print_str]


def request_time(result_response):
    """
    This function return time data using provided weather data. Time is converted form unix time to readable time.
    :param result_response: The weather data
    :return: False if time data retrieval error, else the time data
    """
    try:
        unix_time = result_response['dt']
    except:
        return [False, "Error: Time retrieval error"]

    date = datetime.datetime.utcfromtimestamp(unix_time)
    readable_date = date.strftime('%Y-%m-%d %H:%M:%S +00:00 (UTC)')

    print_str = "The current date and time is " + readable_date
    return [True, print_str]


def request_pressure(result_response):
    """
    This function return pressure data using provided weather data.
    :param result_response: The weather data
    :return: False if pressure data retrieval error, else the pressure data
    """
    try:
        pressure = result_response['main']['pressure']
    except:
        return [False, "Error: Pressure retrieval error"]

    return [True, "Pressure is " + str(pressure) + " hpa"]


def request_cloud(result_response):
    """
    This function return cloud data using provided weather data.
    :param result_response: The weather data
    :return: False if cloud data retrieval error, else the cloud data
    """
    try:
        cloud = result_response['clouds']['all']
    except:
        return [False, "Error: Cloud data retrieval error"]

    return [True, "Cloud: " + str(cloud)]


def request_humidity(result_response):
    """
    This function return humidity data using provided weather data.
    :param result_response: The weather data
    :return: False if humidity data retrieval error, else the humidity data
    """
    try:
        humidity = result_response['main']['humidity']
    except:
        return [False, "Error: Humidity retrieval error"]

    return [True, "Humidity is " + str(humidity)]


def request_wind(result_response):
    """
   This function return wind data using provided weather data.
   :param result_response: The weather data
   :return: False if wind data retrieval error, else the wind data
   """
    try:
        wind_speed = result_response['wind']['speed']
        wind_degree = result_response['wind']['deg']
    except:
        return [False, "Error: Wind data retrieval error"]

    return [True, "Wind speed is " + str(wind_speed) + " at degree of " + str(wind_degree)]


def request_sunset(result_response):
    """
   This function return sunset data using provided weather data. Time is converted to readable time.
   :param result_response: The weather data
   :return: False if sunset data retrieval error, else the sunset data
   """
    try:
        sunset_time = result_response['sys']['sunset']
    except:
        return [False, "Error: Sunset data retrieval error"]

    date = datetime.datetime.utcfromtimestamp(sunset_time)
    readable_date = date.strftime('%Y-%m-%d %H:%M:%S +00:00 (UTC)')

    return [True, "Sunset at " + str(readable_date)]


def request_sunrise(result_response):
    """
   This function return sunrise data using provided weather data. Time is converted to readable time.
   :param result_response: The weather data
   :return: False if sunrise data retrieval error, else the sunrise data
   """
    try:
        sunrise_time = result_response['sys']['sunrise']
    except:
        return [False, "Error: Sunrise data retrieval error"]

    date = datetime.datetime.utcfromtimestamp(sunrise_time)
    readable_date = date.strftime('%Y-%m-%d %H:%M:%S +00:00 (UTC)')

    return [True, "Sunrise at " + str(readable_date)]


def string_concat(main_string, request_string):
    """
    This function concat two string together and place a period symbol at the end.
    :param main_string: The first string
    :param request_string: The second string to be placed behind the first string
    :return: the joined string
    """
    main_string = main_string + request_string + ". "
    return main_string


def weather_retrieve(result, args):
    """
    This function use the weather data and list of arguments within parser namespace to determine which
    data to retrieve, a final string containing all the joined requested data will be returned
    :param result: the weather data
    :param args: arguments stored in a namespace
    :return: True and its weather data in string, else false and its error message
    """
    info_check = False
    request_output = ""

    # cod == 200 indicate successful data retrieval
    if result is not None and result['cod'] == 200:
        # Each arguments is checked, if arguments trigger true, call its corresponding data retrieval function
        # and concat to the mains main string (request_output)
        if args.time:
            temp_storage = request_time(result)
            request_output = string_concat(request_output, temp_storage[1])
            info_check = True

        if args.temp:
            temp_storage = request_temperature(result, args.temp)
            request_output = string_concat(request_output, temp_storage[1])
            info_check = True

        if args.pressure:
            temp_storage = request_pressure(result)
            request_output = string_concat(request_output, temp_storage[1])
            info_check = True

        if args.cloud:
            temp_storage = request_cloud(result)
            request_output = string_concat(request_output, temp_storage[1])
            info_check = True

        if args.humidity:
            temp_storage = request_humidity(result)
            request_output = string_concat(request_output, temp_storage[1])
            info_check = True

        if args.wind:
            temp_storage = request_wind(result)
            request_output = string_concat(request_output, temp_storage[1])
            info_check = True

        if args.sunset:
            temp_storage = request_sunset(result)
            request_output = string_concat(request_output, temp_storage[1])
            info_check = True

        if args.sunrise:
            temp_storage = request_sunrise(result)
            request_output = string_concat(request_output, temp_storage[1])
            info_check = True

        if info_check is False:
            return [False, "No argument chosen to display weather data"]
        else:
            return [True, request_output]
    return [False, "Weather data retrieval error"]


def main(argv):
    """
    This function takes in a list of arguments and process the arguments into a parser namespace, then request the
    weather data based on location type information, the weather data is then printed
    :param argv: a list of arguments
    :return: the output string, can be error messages or weather data
    """
    args = argument_parse(argv)
    key = args.api
    program_output = [False, "No arguments provided"]
    result = None

    if key and args.help:
        # detect the infeasible case of seeking weather data together with request help menu
        program_output = [False, "Program cannot display help and chosen information at the same time"]
    elif key:
        # ensure api provided is correct
        program_output = check_api_key(key)
        if program_output[0] is not False:
            # ensure infeasible case of multiple location provided in detected
            program_output = check_for_location(args)
            if program_output[0] is not False:
                # request weather data based on type of location information provided
                if args.city:
                    result = request_by_city(key, args.city)

                elif args.cid:
                    result = request_by_id(key, args.cid)

                elif args.gc:
                    result = request_by_gc(key, args.gc)

                elif args.z:
                    result = request_by_z(key, args.z)

                # pass the weather data to and weather information requested to weather_retrieve function to
                # filter the weather data and retrieve the required information.
                program_output = weather_retrieve(result, args)
    elif args.help:
        request_help()
        program_output = [True, ""]

    if program_output[0] is not None and program_output[0] is not False:
        # output of weather data without error
        print(program_output[1])
    elif program_output[0] is False:
        # output of data with error message
        print(program_output[1])

    return program_output


if __name__ == '__main__':
    main(sys.argv[1:])




