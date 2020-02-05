from . import *

def resolve(base, href):
  if not is_absolute(base) or not is_well_formed(href):
    return None
  result = []
  type = PathType.APPEND_PATH
  end = href[0][0] if len(href) != 0 else Option.FRAGMENT
  if end == Option.HOST_IP:
    end = Option.HOST_NAME
  elif end == Option.PATH_TYPE:
    type = href[0][1]
    href = href[1:]
    end = Option.QUERY if type > PathType.ABSOLUTE_PATH else Option.PATH
  elif end == Option.PATH:
    type = PathType.RELATIVE_PATH
    end = Option.QUERY
  _copy_until(base, result, end)
  while type > PathType.APPEND_PATH:
    if len(result) == 0 or result[-1][0] != Option.PATH:
      break
    del result[-1]
    type -= 1
  _copy_until(href, result, Option._END)
  _normalize_empty_path(result)
  return result

def _copy_until(source, result, end):
  for option, value in source:
    if option >= end:
      break
    if option > Option.PATH:
      _normalize_empty_path(result)
    result.append((option, value))

def _normalize_empty_path(result):
  if len(result) >= 2 and \
      result[-1] == (Option.PATH, '') and (
      result[-2][0] < Option.PATH_TYPE or (
      result[-2][0] == Option.PATH_TYPE and
      result[-2][1] == PathType.ABSOLUTE_PATH)):
    del result[-1]
