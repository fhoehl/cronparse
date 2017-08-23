import pytest

from cronparse import CronExpression


@pytest.mark.parametrize('expression, output', [
    ('*/15 0 1,15 * 1-5 /usr/bin/find',
     'minute        0 15 30 45\n'
     'hour          0\n'
     'day of month  1 15\n'
     'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
     'day of week   1 2 3 4 5\n'
     'command       /usr/bin/find'),
    ('30 16 * * * tea',
     'minute        30\n'
     'hour          16\n'
     'day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30\n'
     'month         1 2 3 4 5 6 7 8 9 10 11 12\n'
     'day of week   0 1 2 3 4 5 6\n'
     'command       tea'),
])
def test_parse_valid_expression(expression, output):
    cron_expression = CronExpression(expression)
    assert str(cron_expression) == output


@pytest.mark.parametrize('expression', [
    '*/15 0 1,15 * /usr/bin/find',  # Missing day of the week
    '*/15 0 1,15 * 5',  # Missing command
])
def test_parse_invalid_expression(expression):
    with pytest.raises(Exception):
        CronExpression(expression)
