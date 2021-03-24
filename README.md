# pyRailTimes README

[![CI](https://github.com/DoddyUK/pyRailTimes/actions/workflows/run_tests.yml/badge.svg?branch=master)](https://github.com/DoddyUK/pyRailTimes/actions/workflows/run_tests.yml)

pyRailTimes is a command line program that displays a departure board for a given UK railway station,
similar to those seen on platforms. 

## Setup

In order to use this application, you will firstly need to sign up for access to the Realtime Trains API.
You can do so via their [developer portal](https://api.rtt.io/). Once you have done so, rename 
`credentials_example.yaml` to `credentials.yaml` and input your credentials. 

This only makes one request to two endpoints every minute so is not likely to be a drain on this API as things stand,
but please pay attention to the API's T&Cs before using.

Pip requirements are outlines in `requirements.txt`

## Executing

Run `python3 ./TrainDepartures.py`. Use `ctrl + C` to stop the script.

## TODO
* Arrange boards to make use of available width
* Add CANCELLED status
* Take bus replacement services into account

## Other notes

Python isn't my main language so I'm using this project as a learning process. Please be nice, and if you have
any improvements or suggestions then please feel free to put in a pull request :)

## Thanks

With thanks to the [RealTime Trains](https://www.realtimetrains.co.uk/) API team.
