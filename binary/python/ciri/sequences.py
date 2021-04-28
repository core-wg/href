import enum

class Option(enum.IntEnum):
  SCHEME = 0
  HOST_NAME = 1
  HOST_IP = 2
  PORT = 3
  BASE_PATH = 4
  PATH = 5
  QUERY = 6
  FRAGMENT = 7

_TRANSITIONS = ([Option.SCHEME, Option.HOST_NAME, Option.HOST_IP,
  Option.BASE_PATH, Option.PATH, Option.QUERY, Option.FRAGMENT],
  [Option.HOST_NAME, Option.HOST_IP, Option.PATH, Option.QUERY,
  Option.FRAGMENT], [Option.PORT, Option.PATH, Option.QUERY,
  Option.FRAGMENT], [Option.PORT, Option.PATH, Option.QUERY,
  Option.FRAGMENT], [Option.PATH, Option.QUERY, Option.FRAGMENT],
  [Option.PATH, Option.QUERY, Option.FRAGMENT], [Option.PATH,
  Option.QUERY, Option.FRAGMENT], [Option.QUERY, Option.FRAGMENT],
  [])

def is_wellformed(href):
  previous = -1
  for (option, value) in href:
    if option not in _TRANSITIONS[previous + 1]:
      return False
    previous = option
  return True

def is_absolute(href):
  if not is_wellformed(href):
    return False
  return len(href) != 0 and href[0][0] == Option.SCHEME

def is_relative(href):
  if not is_wellformed(href):
    return False
  return len(href) == 0 or href[0][0] != Option.SCHEME
