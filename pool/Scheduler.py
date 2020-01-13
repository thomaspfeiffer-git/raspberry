#!/usr/bin/python3 -u



# install
# sudo pip3 install xmltodict

import operator
import xmltodict

import pprint
pp = pprint.PrettyPrinter(indent=2)


with open('schedule.xml') as fd:
    doc = xmltodict.parse(fd.read())

pp.pprint(doc)


all_conditions = ['time', 'temperature', 'humidity_difference']

def validate_time (start, stop):
    print(f"Start: {start}; stop: {stop}")


def validate_temperature (condition):
    location = condition['@location']
    if location not in ['inside', 'outside']:
        raise ValueError(f"'@location' is '{location}', should be in ['inside', 'outside']")

    value = float(condition['value'])
    if not -10 <= value <= 50:
        raise ValueError(f"'value is '{value}', should be in -10 .. +50")
    condition['value'] = value    

    operator_ = condition['operator']
    if operator_ not in ['<=', '>=']:
        raise ValueError(f"'operator' is '{operator_}', should be in ['<=', '>=']")
    condition['operator'] = {'>=': operator.ge, '<=': operator.le}[operator_]


def validate_humidity_difference (condition):
    value = float(condition['value'])
    if not 1 <= value <= 50:
        raise ValueError(f"'value is '{value}', should be in 1 .. +50")
    condition['value'] = value    

    delay_for_measurement = int(condition['delay_for_measurement'])
    if delay_for_measurement < 1:
        raise ValueError(f"'delay_for_measurement' is '{delay_for_measurement}', should be >= 1")
    condition['delay_for_measurement'] = delay_for_measurement

    delay_for_retry = int(condition['delay_for_retry'])
    if delay_for_retry < 1:
        raise ValueError(f"'delay_for_retry' is '{delay_for_retry}', should be >= 1")
    condition['delay_for_retry'] = delay_for_retry


for schedule in doc['schedules']['schedule']:
    validate_time(schedule['start'], schedule['stop'])

    if 'conditions' in schedule:
        for condition in schedule['conditions']:
            if not condition in all_conditions:
                raise NameError(f"Condition '{condition}' not defined.")
            fn=locals()[f"validate_{condition}"]
            fn(schedule['conditions'][condition])

pp.pprint(doc)

 # eof #

