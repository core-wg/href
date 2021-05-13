from . import *

def resolve(base, href):
  if not is_absolute(base) or not is_wellformed(href):
    return None

  # Determine the values of two variables, T and E, based on the
  # first option in the sequence of options of the CRI reference to
  # be resolved, according to Table 1.
  t = 0
  e = Option.FRAGMENT
  for option, value in href:
    if option == Option.HOST_IP:
      e = Option.HOST_NAME
    elif option == Option.BASE_PATH:
      t = value
      e = Option.QUERY
    else:
      e = option
    break

  # Initialize a buffer with all the options from the base CRI where
  # the option number is less than the value of E.
  result = []
  for option, value in base:
    if option >= e:
      break
    if option > Option.PATH:
      _normalize_empty_path(result)
    result.append((option, value))
  _normalize_empty_path(result)

  # If the value of T is greater than 0, remove the last T-many
  # "path" options from the end of the buffer (up to the number of
  # "path" options in the buffer).
  while t > 0 and result[-1][0] == Option.PATH:
    del result[-1]
    t -= 1

  # Append all the options from the CRI reference to the buffer,
  # excluding any "base-path" option.
  for option, value in href:
    if option > Option.PATH:
      _normalize_empty_path(result)
    if option != Option.BASE_PATH:
      result.append((option, value))
  _normalize_empty_path(result)

  # Return the sequence of options in the buffer as the resolved CRI.
  return result

def _normalize_empty_path(result):
  if len(result) >= 2 and \
      result[-1] == (Option.PATH, '') and \
      result[-2][0] < Option.BASE_PATH:
    del result[-1]
