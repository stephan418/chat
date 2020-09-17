from security.configuration.config import Config
import time

VERBOSE = 0
LOG = 1
WARNING = 2
ERROR = 3
FATAL = 4

error_levels = {
    VERBOSE: 'VERBOSE',
    LOG: 'LOG',
    WARNING: 'WARNING',
    ERROR: 'ERROR',
    FATAL: 'FATAL',
}


def format_msg(level, message: str, f_string: str, customs: list = None):
    format_map = {
        'level': level,
        'level.d': level,
        'level.s': error_levels[level],
        'time': time.strftime('%H:%M:%S'),
        'message': message,
    }

    for key, value in format_map.items():
        f_string = f_string.replace('{' + key + '}', str(value))

    colors = {
        'red': "\u001b[31m",
        'green': "\u001b[32m",
        'yellow': "\u001b[33m",
        'black': "\u001b[30m",
        'blue': "\u001b[34m",
        'magenta': "\u001b[35m",
        'cyan': "\u001b[36m",
        'white': "\u001b[37m",
    }

    levels = []
    color_list = list(map(lambda x: x.split(' ')[0], f_string.split('#')))[1:]
    res = ""
    skip = False
    active = None

    for i, value in enumerate(f_string):
        if value == ' ' and skip:
            skip = False
            continue

        if skip:
            continue

        if levels and active != levels[-1]:
            active = levels[-1]

            if not levels[-1].startswith('custom.'):
                res += colors[levels[-1]]
            else:
                tmp = levels[-1]
                tmp = int(tmp.replace('custom.', ''))

                res += colors[customs[tmp]]

        if value == '{':
            levels.append(color_list.pop(0))
            skip = True

            if not levels[-1].startswith('custom.'):
                res += colors[levels[-1]]
                active = levels[-1]
            else:
                tmp = levels[-1]
                tmp = int(tmp.replace('custom.', ''))

                res += colors[customs[tmp]]
                active = colors[customs[tmp]]

        elif value == '}':
            levels.pop()

            if len(levels) == 0:
                res += "\u001b[0m"
        else:
            res += value

    return res


class Logger:
    def __init__(self, config: Config):
        self.active = config.get('logging', True)
        self.suppress_until = config.get('logging.min_logging_level', VERBOSE)
        self.format = config.get('format', '{#yellow {#custom.0 [{level.s}]} at {time}:} {message}')
        self.level_colors = config.get('level_colors', ['white', 'white', 'yellow', 'red', 'red'])

    def info(self, message):
        if self.active and self.suppress_until <= LOG:
            print(format_msg(VERBOSE, message, self.format, [self.level_colors[VERBOSE]]))

    def log(self, message):
        if self.active and self.suppress_until <= LOG:
            print(format_msg(LOG, message, self.format, [self.level_colors[LOG]]))

    def warn(self, message):
        if self.active and self.suppress_until <= WARNING:
            print(format_msg(WARNING, message, self.format, [self.level_colors[WARNING]]))

    def error(self, message):
        if self.active and self.suppress_until <= ERROR:
            print(format_msg(ERROR, message, self.format, [self.level_colors[ERROR]]))

    def fatal(self, message):
        if self.active:
            print(format_msg(FATAL, message, '{#red [FATAL] at {time}: {message}}'))

