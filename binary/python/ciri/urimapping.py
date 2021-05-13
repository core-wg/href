from . import *

def recompose(href):
  if not is_wellformed(href):
    return None

  result = ''
  path_separator = '/'
  query_separator = '?'

  for option, value in href:
    if option == Option.SCHEME:
      result += value + ':'
      path_separator = ''
    elif option == Option.HOST_NAME:
      result += '//' + _encode_reg_name(value)
      path_separator = '/'
    elif option == Option.HOST_IP:
      result += '//' + _encode_ip_address(value)
      path_separator = '/'
    elif option == Option.PORT:
      result += ':' + _encode_port(value)
    elif option == Option.BASE_PATH:
      return None
    elif option == Option.PATH:
      result += path_separator + _encode_path_segment(value)
      path_separator = '/'
    elif option == Option.QUERY:
      result += query_separator + _encode_query_argument(value)
      query_separator = '&'
    elif option == Option.FRAGMENT:
      result += '#' + _encode_fragment(value)

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
