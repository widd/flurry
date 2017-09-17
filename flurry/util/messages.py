_error_template = '%xt%e%0%{0}%'
_error_arg_template = _error_template + '{1}%'

# Per https://github.com/widd/cp-protocol/blob/master/as2/server/errors.md#error-ids
PENGUIN_NOT_FOUND = _error_template.format(100)
INCORRECT_PASSWORD = _error_template.format(101)
LOGIN_FLOODING = _error_template.format(150)
BAN_DURATION = lambda d: _error_arg_template.format(601, d)
BAN_AN_HOUR = _error_template.format(602)
BANNED_FOREVER = _error_template.format(603)

LOGIN_KEY = lambda i, k: '%xt%l%0%{0}%{1}%'.format(i, k)
