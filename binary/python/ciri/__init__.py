# Copyright (c) IETF Trust and the persons identified as authors of the code.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, is permitted pursuant to, and subject to the license terms
# contained in, the Simplified BSD License set forth in Section 4.c of the IETF
# Trust’s Legal Provisions Relating to IETF Documents
# (http://trustee.ietf.org/license-info).

import enum, ipaddress

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
  APPEND_RELATION = 1
  APPEND_PATH = 2
  RELATIVE_PATH = 3
  RELATIVE_PATH_1UP = 4
  RELATIVE_PATH_2UP = 5
  RELATIVE_PATH_3UP = 6
  RELATIVE_PATH_4UP = 7

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

def resolve(base, href, relation=0):
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
    if type == PathType.APPEND_RELATION:
      _append_and_normalize(result, Option.PATH, str(relation))
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

def recompose(href):
  if not is_absolute(href):
    return None
  result = ''
  no_path = True
  first_query = True
  for option, value in href:
    if option == Option.SCHEME:
      result += value + ':'
    elif option == Option.HOST_NAME:
      result += '//' + _encode_reg_name(value)
    elif option == Option.HOST_IP:
      result += '//' + _encode_ip_address(value)
    elif option == Option.PORT:
      result += ':' + _encode_port(value)
    elif option == Option.PATH:
      result += '/' + _encode_path_segment(value)
      no_path = False
    elif option == Option.QUERY:
      if no_path:
        result += '/'
        no_path = False
      result += '?' if first_query else '&'
      result += _encode_query_argument(value)
      first_query = False
    elif option == Option.FRAGMENT:
      if no_path:
        result += '/'
        no_path = False
      result += '#' + _encode_fragment(value)
  if no_path:
    result += '/'
    no_path = False
  return result

def _encode_reg_name(s):
  return ''.join(c if _is_reg_name_char(c)
                   else _encode_pct(c) for c in s)

def _encode_ip_address(b):
  if len(b) == 4:
    return '.'.join(str(c) for c in b)
  elif len(b) == 16:
    return '[' + str(ipaddress.IPv6Address(b)) + ']'  # see RFC 5952

def _encode_port(p):
   return str(p)

def _encode_path_segment(s):
  return ''.join(c if _is_segment_char(c)
                   else _encode_pct(c) for c in s)

def _encode_query_argument(s):
  return ''.join(c if _is_query_char(c) and c not in '&'
                   else _encode_pct(c) for c in s)

def _encode_fragment(s):
  return ''.join(c if _is_fragment_char(c)
                   else _encode_pct(c) for c in s)

def _encode_pct(s):
  return ''.join('%{0:0>2X}'.format(c) for c in s.encode('utf-8'))

def _is_reg_name_char(c):
  return _is_unreserved(c) or _is_sub_delim(c)

def _is_segment_char(c):
  return _is_pchar(c)

def _is_query_char(c):
  return _is_pchar(c) or c in '/?'

def _is_fragment_char(c):
  return _is_pchar(c) or c in '/?'

def _is_pchar(c):
  return _is_unreserved(c) or _is_sub_delim(c) or c in ':@'

def _is_unreserved(c):
  return _is_alpha(c) or _is_digit(c) or c in '-._~'

def _is_alpha(c):
  return c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + \
              'abcdefghijklmnopqrstuvwxyz'

def _is_digit(c):
  return c in '0123456789'

def _is_sub_delim(c):
   return c in '!$&\'()*+,;='

def coap(href, to_proxy=False):
  if not is_absolute(href):
    return None
  result = b''
  previous = 0
  for option, value in href:
    if option == Option.SCHEME:
      pass
    elif option == Option.HOST_NAME:
      opt = 3  # Uri-Host
      val = value.encode('utf-8')
      result += _encode_coap_option(opt - previous, val)
      previous = opt
    elif option == Option.HOST_IP:
      opt = 3  # Uri-Host
      if len(value) == 4:
        val = '.'.join(str(c) for c in value).encode('utf-8')
      elif len(value) == 16:
        val = b'[' + str(ipaddress.IPv6Address(b)).encode('utf-8') + b']'  # see RFC 5952
      result += _encode_coap_option(opt - previous, val)
      previous = opt
    elif option == Option.PORT:
      opt = 7  # Uri-Port
      val = value.to_bytes((value.bit_length() + 7) // 8, 'big')
      result += _encode_coap_option(opt - previous, val)
      previous = opt
    elif option == Option.PATH:
      opt = 11  # Uri-Path
      val = value.encode('utf-8')
      result += _encode_coap_option(opt - previous, val)
      previous = opt
    elif option == Option.QUERY:
      opt = 15  # Uri-Query
      val = value.encode('utf-8')
      result += _encode_coap_option(opt - previous, val)
      previous = opt
    elif option == Option.FRAGMENT:
      pass
  if to_proxy:
    (option, value) = href[0]
    opt = 39  # Proxy-Scheme
    val = value.encode('utf-8')
    result += _encode_coap_option(opt - previous, val)
    previous = opt
  return result

def _encode_coap_option(delta, value):
  length = len(value)
  delta_nibble = _encode_coap_option_nibble(delta)
  length_nibble = _encode_coap_option_nibble(length)
  result = bytes([delta_nibble << 4 | length_nibble])
  if delta_nibble == 13:
    delta -= 13
    result += bytes([delta])
  elif delta_nibble == 14:
    delta -= 256 + 13
    result += bytes([delta >> 8, delta & 255])
  if length_nibble == 13:
    length -= 13
    result += bytes([length])
  elif length_nibble == 14:
    length -= 256 + 13
    result += bytes([length >> 8, length & 255])
  result += value
  return result

def _encode_coap_option_nibble(n):
  if n < 13:
    return n
  elif n < 256 + 13:
    return 13
  elif n < 65536 + 256 + 13:
    return 14
