from . import *

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
    return '[' + rfc5952str(b) + ']'

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
