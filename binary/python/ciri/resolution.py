from . import *

def resolve(base, href):
  if not is_absolute(base) or not is_well_formed(href):
    return None
  result = []
  option = Option.FRAGMENT
  if len(href) != 0:
    option = href[0][0]
  if option == Option.HOST_IP:
    option = Option.HOST_NAME
  elif option == Option.PATH_TYPE:
    type = href[0][1]
    href = href[1:]
  elif option == Option.PATH:
    type = PathType.RELATIVE_PATH
    option = Option.PATH_TYPE
  if option != Option.PATH_TYPE or type == PathType.ABSOLUTE_PATH:
    _copy_until(base, result, option)
  else:
    _copy_until(base, result, Option.QUERY)
    while type > PathType.APPEND_PATH:
      if len(result) == 0 or result[-1][0] != Option.PATH:
        break
      del result[-1]
      type -= 1
  _copy_until(href, result, Option._END)
  _append_and_normalize(result, Option._END, None)
  return result

def _copy_until(input, output, end):
  for option, value in input:
    if option >= end:
      break
    _append_and_normalize(output, option, value)

def _append_and_normalize(output, option, value):
  if option > Option.PATH:
    if len(output) >= 2 and \
        output[-1] == (Option.PATH, '') and (
        output[-2][0] < Option.PATH_TYPE or (
        output[-2][0] == Option.PATH_TYPE and
        output[-2][1] == PathType.ABSOLUTE_PATH)):
      del output[-1]
    if option > Option.FRAGMENT:
      return
  output.append((option, value))
