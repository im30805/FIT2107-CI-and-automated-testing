import unittest
import WeatherForecast
from unittest.mock import Mock, patch

key = '241662d8c926c731d81cddf5e783f8d8'


class TestWeatherForecast(unittest.TestCase):
    def setUp(self):
        # Set up of weather data using mock. Mocking of the actual weather data is then returned when the mocked
        # variable is called.
        self.weather_data = Mock()
        self.weather_data_failed = Mock()

        # Act as complete data
        self.weather_data.return_value = {"coord":{"lon":-0.15,"lat":49.70},
                               "weather":[
                                   {"id":300,
                                    "main":"Drizzle",
                                    "description":"light intensity drizzle",
                                    "icon":"09d"}
                               ],
                               "base":"stations",
                               "main":{
                                   "temp":270.23,
                                   "pressure":1009,
                                   "humidity":72,
                                   "temp_min":269.15,
                                   "temp_max":278.15
                               },
                               "visibility":10000,
                               "wind":{
                                   "speed":3.1,
                                   "deg":82
                               },
                               "clouds":{
                                   "all":90
                               },
                               "dt":1485789600,
                               "sys":{
                                   "type":1,
                                   "id":5091,
                                   "message":0.0103,
                                   "country":"GB",
                                   "sunrise":1485762037,
                                   "sunset":1485794875
                               },
                               "id":2643743,
                               "name":"London",
                               "cod":200
                               }

        # Act as data with failed weather data retrieval
        self.weather_data_failed.return_value = {'cod': '404', 'message': 'fail message example'}

    def test_request_by_city(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_by_city(key, 'Kuala Lumpur')['cod'], 200)
        # Test invalid case
        self.assertEqual(WeatherForecast.request_by_city(key, 'FalseCountry'), None)

    def test_request_by_id(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_by_id(key, '2172797')['cod'], 200)
        # Test invalid case
        self.assertEqual(WeatherForecast.request_by_id(key, '888888888888'), None)

    def test_request_by_gc(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_by_gc(key, '3.1390,101.6869')['cod'], 200)
        # Test invalid case
        self.assertEqual(WeatherForecast.request_by_gc(key, '1211,2334'), None)

    def test_request_by_z(self):
        # Test valid case type 1
        self.assertEqual(WeatherForecast.request_by_z(key, '47810,my')['cod'], 200)
        # Test valid case type 2
        self.assertEqual(WeatherForecast.request_by_z(key, '99501')['cod'], 200)
        # Test invalid case
        self.assertEqual(WeatherForecast.request_by_z(key, '47810'), None)

    def test_temp(self):
        # Test valid case for celsius request
        self.assertEqual(WeatherForecast.request_temperature(self.weather_data(), 'Celsius'),
                         [True, "The temperature ranges from 269.15 C-278.15 C"])
        # Test valid case for fahrenheit request
        self.assertEqual(WeatherForecast.request_temperature(self.weather_data(), 'Fahrenheit'),
                         [True, "The temperature ranges from 516.47 F-532.67 F"])
        # Test invalid case
        self.assertEqual(WeatherForecast.request_temperature(self.weather_data(), 'Kelvin'),
                         [False, "Invalid temperature format entered: temperature unable to display"])
        # Test invalid case with failed weather data
        self.assertEqual(WeatherForecast.request_temperature(self.weather_data_failed(), 'Celsius'),
                         [False, "Error: Temperature retrieval error"])

    def test_time(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_time(self.weather_data()),
                         [True, "The current date and time is 2017-01-30 15:20:00 +00:00 (UTC)"])
        # Test invalid case
        self.assertEqual(WeatherForecast.request_time(self.weather_data_failed()),
                         [False, "Error: Time retrieval error"])

    def test_pressure(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_pressure(self.weather_data()), [True, "Pressure is 1009 hpa"])
        # Test invalid case
        self.assertEqual(WeatherForecast.request_pressure(self.weather_data_failed()),
                         [False, "Error: Pressure retrieval error"])

    def test_cloud(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_cloud(self.weather_data()), [True, "Cloud: 90"])
        # Test invalid case
        self.assertEqual(WeatherForecast.request_cloud(self.weather_data_failed()),
                         [False, "Error: Cloud data retrieval error"])

    def test_humidity(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_humidity(self.weather_data()), [True, "Humidity is 72"])
        # Test invalid case
        self.assertEqual(WeatherForecast.request_humidity(self.weather_data_failed()),
                         [False, "Error: Humidity retrieval error"])

    def test_wind(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_wind(self.weather_data()), [True, "Wind speed is " + str(3.1)
                                                                             + " at degree of " + str(82)])
        # Test invalid case
        self.assertEqual(WeatherForecast.request_wind(self.weather_data_failed()),
                         [False, "Error: Wind data retrieval error"])

    def test_sunset(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_sunset(self.weather_data()),
                         [True, 'Sunset at 2017-01-30 16:47:55 +00:00 (UTC)'])
        # Test invalid case
        self.assertEqual(WeatherForecast.request_sunset(self.weather_data_failed()),
                         [False, "Error: Sunset data retrieval error"])

    def test_sunrise(self):
        # Test valid case
        self.assertEqual(WeatherForecast.request_sunrise(self.weather_data()),
                         [True, 'Sunrise at 2017-01-30 07:40:37 +00:00 (UTC)'])
        # Test invalid case
        self.assertEqual(WeatherForecast.request_sunrise(self.weather_data_failed()),
                         [False, "Error: Sunrise data retrieval error"])

    def test_argument_parse(self):
        # Test that all acceptable arguments are accepted and saved properly into the parser arguments namespace.
        arguments = WeatherForecast.argument_parse(['-api="241662d8c926c731d81cddf5e783f8d8"', '-city="London"',
                                                    '-time', '-temp', '-pressure', '-cloud', '-humidity', '-wind',
                                                    '-sunset', '-sunrise'])
        self.assertTrue(arguments.api)
        self.assertTrue(arguments.city)
        self.assertTrue(arguments.time)
        self.assertTrue(arguments.temp)
        self.assertTrue(arguments.pressure)
        self.assertTrue(arguments.cloud)
        self.assertTrue(arguments.humidity)
        self.assertTrue(arguments.wind)
        self.assertTrue(arguments.sunset)
        self.assertTrue(arguments.sunrise)

    def test_parse_help_call(self):
        self.assertTrue(WeatherForecast.request_help())

    def test_check_api_key(self):
        # Test valid case
        self.assertEqual(WeatherForecast.check_api_key('241662d8c926c731d81cddf5e783f8d8'), [True, ""])
        # Test invalid case
        self.assertEqual(WeatherForecast.check_api_key('123'), [False, "API key error: " +
                  "Invalid API key. Please see " + 'http://openweathermap.org/faq#error401 for more info.'])

    def test_check_for_location(self):
        # Test valid case
        arguments = WeatherForecast.argument_parse(['-api="241662d8c926c731d81cddf5e783f8d8"', '-city="London"'])
        self.assertEqual(WeatherForecast.check_for_location(arguments), [True, ""])

        # Test invalid case type 1 - no location provided
        arguments = WeatherForecast.argument_parse(['-api="241662d8c926c731d81cddf5e783f8d8"'])
        self.assertEqual(WeatherForecast.check_for_location(arguments), [False, "No location specified"])

        # Test invalid case type 2 - more than 1 location provided
        arguments = WeatherForecast.argument_parse(['-api="241662d8c926c731d81cddf5e783f8d8"', '-city="London"',
                                                    '-z=99501', '-gc=3.1390,101.6869', '-cid=2172797'])
        self.assertEqual(WeatherForecast.check_for_location(arguments),
                         [False, "Multiple chosen locations are specified"])

    def test_string_concat(self):
        self.assertEqual(WeatherForecast.string_concat("test", "concat"), "testconcat. ")

    def test_weather_retrieve(self):
        # Test valid case
        arguments = WeatherForecast.argument_parse(['-api="241662d8c926c731d81cddf5e783f8d8"', '-city="London"',
                                                    '-time', '-temp', '-pressure', '-cloud', '-humidity', '-wind',
                                                    '-sunset', '-sunrise'])
        self.assertTrue(WeatherForecast.weather_retrieve(self.weather_data(), arguments)[0])

        # Test invalid case type 1 - not weather information requested given a location to check its weather data
        arguments = WeatherForecast.argument_parse(['-api="241662d8c926c731d81cddf5e783f8d8"', '-city="London"'])
        self.assertEqual(WeatherForecast.weather_retrieve(self.weather_data(), arguments),
                         [False, "No argument chosen to display weather data"])

        # Test invalid case type 2 - passing an invalid weather data
        self.assertEqual(WeatherForecast.weather_retrieve(self.weather_data_failed(), arguments),
                         [False, "Weather data retrieval error"])

    def test_main(self):
        # Test invalid case type 1 - asking for weather information and requesting help at the same time
        test_argument = ['-api=241662d8c926c731d81cddf5e783f8d8', '-city=London', '-time', '-help']
        self.assertEqual(WeatherForecast.main(test_argument),
                         [False, "Program cannot display help and chosen information at the same time"])

        # Test valid case type 1 - only -help argument is requested.
        test_argument = ['-help']
        self.assertEqual(WeatherForecast.main(test_argument),
                         [True, ""])

        # Test invalid case type 2 - providing bad api
        test_argument = ['-api=123', '-city=London', '-time']
        self.assertEqual(WeatherForecast.main(test_argument), [False, "API key error: " +
                  "Invalid API key. Please see " + 'http://openweathermap.org/faq#error401 for more info.'])

        # Test valid case type 2 - proper api key and weather data request
        test_argument = ['-api=241662d8c926c731d81cddf5e783f8d8', '-city=London', '-time']
        self.assertTrue(WeatherForecast.main(test_argument)[0])

        # Test invalid case type 3 - infeasible case, multiple location provided
        test_argument = ['-api=241662d8c926c731d81cddf5e783f8d8', '-city=London', '-z=99501',
                         '-time']
        self.assertEqual(WeatherForecast.main(test_argument), [False, 'Multiple chosen locations are specified'])

        # Test valid case - request using city name
        test_argument = ['-api=241662d8c926c731d81cddf5e783f8d8', '-city=London', '-time']
        self.assertTrue(WeatherForecast.main(test_argument)[0])

        # Test valid case - request using city ID
        test_argument = ['-api=241662d8c926c731d81cddf5e783f8d8', '-cid=2172797', '-time']
        self.assertTrue(WeatherForecast.main(test_argument)[0])

        # Test valid case - request using coordinate
        test_argument = ['-api=241662d8c926c731d81cddf5e783f8d8', '-gc=3.1390,101.6869', '-time']
        self.assertTrue(WeatherForecast.main(test_argument)[0])

        # Test valid case - request using zip code
        test_argument = ['-api=241662d8c926c731d81cddf5e783f8d8', '-z=47810,my', '-time']
        self.assertTrue(WeatherForecast.main(test_argument)[0])

        # Test invalid case type 4, no arguments provided
        test = []
        self.assertEqual(WeatherForecast.main(test), [False, "No arguments provided"])


if __name__ == '__main__':
    unittest.main()
