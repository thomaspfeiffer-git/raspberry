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
        raise ValueError() # TODO

    value = float(condition['value'])
    if not -10 <= value <= 50:
        raise ValueError() # TODO

    operator = condition['operator']
    if operator not in ["<=", ">="]:
        raise ValueError() # TODO

    print(f"location: {location}, value: {value}, operator: {operator}")    

def validate_humidity_difference (condition):
    print(f"in validate_humidity_difference: {condition}")


for s in doc['schedules']['schedule']:
    validate_time(s['start'], s['stop'])

    if 'conditions' in s:
        for condition in s['conditions']:
            if not condition in validators:
                raise NameError(f"Condition '{condition}' not defined.")
            fn=locals()[f"validate_{condition}"]
            fn(s['conditions'][condition])

 # eof #

