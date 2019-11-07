# Cron Expression Parser

A simple cron expression parser implemented in Python. 

## Instructions
In order to run the parser, make sure that you are in the root directory of the project and have python 3.8 installed.  
The program takes in a single argument encapsulated in a string:  
`python cron_parser.py "<cron string here>"`

The argument should contain a cron string of the format:
`<minute> <hour> <day of month> <month> <day of week> <command>`

If run with valid input, the program will print out a table describing the expression on a per attribute basis.  

Running the following command `*/15 0 1,15 * 1-5 /usr/bin/find` will produce the following output:
```
minute: 0 15 30 45  
hour: 0  
day of month: 1 15  
month: 1 2 3 4 5 6 7 8 9 10 11 12  
day of week: 1 2 3 4 5  
command: /usr/bin/find
```

The characters and values each field can contain are as thus:  
minute: `, - * /` with the values `0-59` inclusive  
hour: `, - * /` with the values `0-23` inclusive  
day of month: `, - * / ? W` with the values `1-31` inclusive  
month: `, - * /` with the values `1-12` inclusive or `JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC`  
day of week: `, - * ? /` with the values `1-7` inclusive or `SUN, MON, TUE, WED, THU, FRI, SAT`  

## Tests
Basic unit tests for the parser have been written to ensure it works as expected.  
These can be run with the following command:
`python CronParserTest.py`

## Todo
- Implement remaining cron expressions such as `#` `L` `C`
- Use a date package to validate day of month input, i.e. 31st February would be invalid  
- Add more in depth unit tests in order to ensure that exceptions are being raised correctly

For a more information and examples of cron expressions, please visit [CRON Expression wiki](http://docwiki.embarcadero.com/Connect/en/Writing_a_CRON_Expression)
