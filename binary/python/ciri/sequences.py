import enum

class Option(enum.IntEnum):
  _BEGIN = 0
  SCHEME = 1
  HOST_NAME = 2
  HOST_IP = 3
  PORT = 4
  PATH_TYPE = 5
  PATH = 6
  QUERY = 7
  FRAGMENT = 8
  _END = 9

class PathType(enum.IntEnum):
  ABSOLUTE_PATH = 0
  APPEND_PATH = 1
  RELATIVE_PATH = 2
  RELATIVE_PATH_1UP = 3
  RELATIVE_PATH_2UP = 4
  RELATIVE_PATH_3UP = 5
  RELATIVE_PATH_4UP = 6

_TRANSITIONS = ([Option.SCHEME, Option.HOST_NAME, Option.HOST_IP,
    Option.PORT, Option.PATH_TYPE, Option.PATH, Option.QUERY,
    Option.FRAGMENT, Option._END],
  [Option.HOST_NAME, Option.HOST_IP],
  [Option.PORT],
  [Option.PORT],
  [Option.PATH, Option.QUERY, Option.FRAGMENT, Option._END],
  [Option.PATH, Option.QUERY, Option.FRAGMENT, Option._END],
  [Option.PATH, Option.QUERY, Option.FRAGMENT, Option._END],
  [Option.QUERY, Option.FRAGMENT, Option._END],
  [Option._END])

def is_well_formed(href):
  previous = Option._BEGIN
  for option, _ in href:
    if option not in _TRANSITIONS[previous]:
      return False
    previous = option
  if Option._END not in _TRANSITIONS[previous]:
    return False
  return True

def is_absolute(href):
  return is_well_formed(href) and \
    (len(href) != 0 and href[0][0] == Option.SCHEME)

def is_relative(href):
  return is_well_formed(href) and \
    (len(href) == 0 or href[0][0] != Option.SCHEME)
