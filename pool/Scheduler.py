#!/usr/bin/python3 -u



# install
# sudo pip3 install xmltodict

import xmltodict

import pprint
pp = pprint.PrettyPrinter(indent=2)


with open('schedule.xml') as fd:
    doc = xmltodict.parse(fd.read())

pp.pprint(doc)


validators = ['time', 'temperature', 'humidity_difference']

def validate_time (start, stop):
    print(f"Start: {start}; stop: {stop}")

def validate_temperature (condition):
    location = condition['@location']
    if location not in ['inside', 'outside']:
        raise ValueError(f"'@location' is '{location}', should be in ['inside', 'outside']")

    value = float(condition['value'])
    if not -10 <= value <= 50:
        raise ValueError(f"'value is '{value}', should be in -10 .. +50")

    operator = condition['operator']
    if operator not in ['<=', '>=']:
        raise ValueError(f"'operator' is '{operator}', should be in ['<=', '>=']")

    print(f"location: {location}, value: {value}, operator: {operator}")    

def validate_humidity_difference (condition):
    value = float(condition['value'])
    if not 1 <= value <= 50:
        raise ValueError(f"'value is '{value}', should be in 1 .. +50")

    delay_for_measurement = int(condition['delay_for_measurement'])
    if delay_for_measurement < 1:
        raise ValueError() # TODO

    delay_for_retry = int(condition['delay_for_retry'])
    if delay_for_retry < 1:
        raise ValueError() # TODO

    print(f"value: {value}, delay_for_measurement: {delay_for_measurement}, delay_for_retry: {delay_for_retry}")    


for s in doc['schedules']['schedule']:
    validate_time(s['start'], s['stop'])

    if 'conditions' in s:
        for condition in s['conditions']:
            if not condition in validators:
                raise NameError(f"Condition '{condition}' not defined.")
            fn=locals()[f"validate_{condition}"]
            fn(s['conditions'][condition])

 # eof #

