from . import *

def resolve(base, href):
  if not is_absolute(base) or not is_wellformed(href):
    return None

  result = []

  e = Option.FRAGMENT
  t = 0
  for option, value in href:
    if option == Option.HOST_IP:
      e = Option.HOST_NAME
    elif option == Option.BASE_PATH:
      e = Option.QUERY if value > 0 else Option.PATH
      t = value
    elif option == Option.PATH:
      e = Option.QUERY
    else:
      e = option
    break

  for option, value in base:
    if option >= e:
      break
    if option > Option.PATH:
      _normalize_empty_path(result)
    result.append((option, value))
  _normalize_empty_path(result)

  while t > 0 and result[-1][0] == Option.PATH:
    del result[-1]
    t -= 1

  for option, value in href:
    if option > Option.PATH:
      _normalize_empty_path(result)
    if option != Option.BASE_PATH:
      result.append((option, value))
  _normalize_empty_path(result)

  return result

def _normalize_empty_path(result):
  if len(result) >= 2 and \
      result[-1] == (Option.PATH, '') and \
      result[-2][0] < Option.BASE_PATH:
    del result[-1]
