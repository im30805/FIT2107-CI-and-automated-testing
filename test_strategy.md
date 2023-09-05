Test strategy

The white-box techniques used to determine the test cases for the WeatherForecast program are mainly statement coverage and branch coverage. 

Each command-line argument has its own test case in the TestWeatherForecast file to allow all statements in each function for each argument is able to execute at least once. This would allow us to roughly know that the program is able to run and cover most of the code. However, it is not sufficient enough to see if the behaviour of each functionality is working as intended as well as the error handling of the program.

In order to accurately test the behaviour and error handling, branch/decision coverage is also used to help improve and add more to our test cases. As a user can choose any combination of weather information they want to view, this would allow us to consider as many possible paths (if-else, try and except) in the code. For the mandatory inputs (API key and location) there are also decisions to be made here where a user may enter more than one format of location, or an invalid API key. Hence, each decision has a true and a false outcome depending on the inputs and the information chosen (if the required arguments are valid). In the WeatherForecast program, when the user chooses a location format to input, if no message is displayed the response is valid, but otherwise an error message will display and the response will be None. Each weather request will return true and the chosen information and false along with an error message if it cannot retrieve the data. 

Therefore, our test cases involve using assertions to check for the possible combinations of input and the return result in the scenario of valid and invalid cases. Mocking was also used in the test cases to mimic the API requests in order to reduce the time taken to run the tests as well as to test that the functions in the code work as they should. By making an actual API call once to see how the data is shown, the data used for testing is mocked accordingly.









