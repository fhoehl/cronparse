#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Parse a cron expression and output a friendly summary

 ┌───────────── minute (0 - 59)
 │ ┌─────────── hour (0 - 23)
 │ │ ┌───────── day of month (1 - 31)
 │ │ │ ┌─────── month (1 - 12)
 │ │ │ │ ┌───── day of week (0 - 6)
 │ │ │ │ │
 * * * * *  command to execute
'''

import argparse
import re
from functools import partial

OUTPUT_FORMAT = 'minute        {}\n'\
                'hour          {}\n'\
                'day of month  {}\n'\
                'month         {}\n'\
                'day of week   {}\n'\
                'command       {}'

WILDCARD_INTERVAL_RE = '\*\/([0-9]+)$'
NUMBER_SINGLE_RE = '([0-9]+)$'
NUMBER_LIST_RE = '([0-9](?:,[0-9]+)*)$'
NUMBER_RANGE_RE = '([0-9]+)\-([0-9]+)$'


def parse_wildcard_interval(expression, minimun=0, maximum=61):
    '''Parse interval with step value e.g */15
    Returns an array with the number included in the interval.
    '''

    match = re.match(WILDCARD_INTERVAL_RE, expression)

    if match:
        interval_number = match.group(1)
        return range(minimun, maximum, int(interval_number))


def parse_number_single(expression):
    '''Parse single number'''

    match = re.match(NUMBER_SINGLE_RE, expression)

    if match:
        return [int(match.group(0))]


def parse_number_list(expression):
    '''Parse number list e.g. 1,2,3
    Returns an array with the number in the specified list.
    '''

    match = re.match(NUMBER_LIST_RE, expression)

    if match:
        numbers = match.group(0).split(',')
        return [int(number) for number in numbers]


def parse_number_range(expression):
    '''Parse number range e.g. 1-15
    Returns an array with the numbers include in the range.
    '''

    match = re.match(NUMBER_RANGE_RE, expression)

    if match:
        low = int(match.group(1))
        high = int(match.group(2))

        return range(low, high + 1)


def parse_minute(expression):
    parsers = (
        partial(parse_wildcard_interval, minimun=0, maximum=60),
        parse_number_single, parse_number_list, parse_number_range,
    )

    if expression == '*':
        return range(0, 60)

    for parse_fn in parsers:
        result = parse_fn(expression)
        if result:
            return list(result)

    raise ValueError('Bad format')


def parse_hour(expression):
    parsers = (
        partial(parse_wildcard_interval, minimun=0, maximum=24),
        parse_number_single, parse_number_list, parse_number_range,
    )

    if expression == '*':
        return range(0, 25)

    for parse_fn in parsers:
        result = parse_fn(expression)
        if result:
            return list(result)

    raise ValueError('Bad format')


def parse_day_of_month(expression):
    parsers = (
        partial(parse_wildcard_interval, minimun=1, maximum=32),
        parse_number_single, parse_number_list, parse_number_range,
    )

    if expression == '*':
        return range(1, 31)

    for parse_fn in parsers:
        result = parse_fn(expression)
        if result:
            return list(result)

    raise ValueError('Bad format')


def parse_month(expression):
    parsers = (
        partial(parse_wildcard_interval, minimun=1, maximum=13),
        parse_number_single, parse_number_list, parse_number_range,
    )

    if expression == '*':
        return range(1, 13)

    for parse_fn in parsers:
        result = parse_fn(expression)
        if result:
            return list(result)

    raise ValueError('Bad format')


def parse_day_of_week(expression):
    parsers = (
        partial(parse_wildcard_interval, minimun=0, maximum=7),
        parse_number_single, parse_number_list, parse_number_range,
    )

    if expression == '*':
        return range(0, 7)

    for parse_fn in parsers:
        result = parse_fn(expression)
        if result:
            return list(result)

    raise ValueError('Bad format')


class CronExpression(object):
    def __init__(self, cron_string):
        try:
            minute, hour, day_of_month, month, day_of_week, command = cron_string.split(' ')
            self.minute = parse_minute(minute)
            self.hour = parse_hour(hour)
            self.day_of_month = parse_day_of_month(day_of_month)
            self.month = parse_month(month)
            self.day_of_week = parse_day_of_week(day_of_week)
            self.command = command
        except ValueError:
            raise ValueError('Bad format')

    def __str__(self):
        output = OUTPUT_FORMAT.format(
            ' '.join(map(str, self.minute)),
            ' '.join(map(str, self.hour)),
            ' '.join(map(str, self.day_of_month)),
            ' '.join(map(str, self.month)),
            ' '.join(map(str, self.day_of_week)),
            self.command)
        return output


def main():
    """Main"""

    parser = argparse.ArgumentParser(
        description='Parse a cron expression and output a friendly summary'
    )

    parser.add_argument('cron_string', help='Cron expression')
    args = parser.parse_args()
    cron_expression = CronExpression(args.cron_string)
    print(cron_expression)


if __name__ == '__main__':
    main()
