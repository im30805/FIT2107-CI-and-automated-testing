# project

FIT2107 project repository

*IMPORTANT
Before running the program, please ensure the following module/package installed.
List shown with pip install command.<br />


1.  pip install requests
2.  pip install urllib3
3.  pip install datetime
4.  pip install argparse
5.  pip install coverage

After installing the required module/package, below are example how to run the
program WeatherForecast.py<br />

In the terminal, insert the command<br />

python WeatherForecast.py<br />

After that, there are list of arguments that can be provided, to know its
acceptable arguments, run this command<br />

python WeatherForecast.py -help<br />

*note that valid API and location must be provided to retrieve information correctly.<br />

Below are several example of running the program to display weather data<br />

Scenario 1: Requesting London and its time<br />
python WeatherForecast.py -api="241662d8c926c731d81cddf5e783f8d8" -city="London" -time<br />

Scenario 2: Requesting London and its time, humidity, and pressure<br />
python WeatherForecast.py -api="241662d8c926c731d81cddf5e783f8d8" -city="London" -time -humidity -pressure

Scenario 3: Requesting London and its temperature in celsius<br />
python WeatherForecast.py -api="241662d8c926c731d81cddf5e783f8d8" -city="London" -temp="Celsius"<br />

Scenario 4: Requesting London and all its available weather data<br />
python WeatherForecast.py -api="241662d8c926c731d81cddf5e783f8d8" -city="London" -time -temp -pressure -cloud -humidity -wind -sunset -sunrise<br />
